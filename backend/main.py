"""
FastAPI backend for AllerSafe - Food Allergy Detection Service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from allergen_detector.allergen_detector import detect_allergens
from alternative_finder.alternative_finder import find_alternatives
from product_analyzer import analyze_product
from utils import clean_sources_list
import boto3
import tempfile
import os
import traceback
import json
import asyncio
import queue
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AllerSafe API",
    description="Food allergy detection and safe alternative finder",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class AllergenDetectionRequest(BaseModel):
    s3_image_url: str = Field(..., description="S3 URL of the product image")
    allergens: List[str] = Field(..., description="List of allergens to check for")

    class Config:
        json_schema_extra = {
            "example": {
                "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
                "allergens": ["Milk", "Peanuts", "Eggs"]
            }
        }


class AllergenDetectionResponse(BaseModel):
    severity: str = Field(..., description="Risk level: Safe, Caution, or Dangerous")
    allergens_detected: List[str] = Field(..., description="List of detected allergens")
    warnings: str = Field(..., description="Detailed explanation of the analysis")
    product_name: Optional[str] = Field(None, description="Identified product name")
    sources: Optional[List[dict]] = Field(None, description="Research sources cited")


class AlternativeProduct(BaseModel):
    alternative_name: str = Field(..., description="Specific product name with brand")
    company: str = Field(..., description="Manufacturer name")
    image_url: Optional[str] = Field(None, description="Direct URL to product image")
    purchase_links: List[str] = Field(..., description="Links to purchase the product")
    price: str = Field(..., description="Price in USD")
    warning_level: str = Field(..., description="Safety level: Safe or Caution")
    tags: List[str] = Field(..., description="Descriptive tags (max 3)")
    reasoning: Optional[str] = Field(None, description="Explanation of why this alternative was chosen")
    sources: Optional[List[dict]] = Field(None, description="Research sources for this alternative")


class AlternativeFinderRequest(BaseModel):
    s3_image_url: str = Field(..., description="S3 URL of the product image")
    allergens: List[str] = Field(..., description="List of allergens to avoid")

    class Config:
        json_schema_extra = {
            "example": {
                "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
                "allergens": ["Milk", "Peanuts", "Gluten"]
            }
        }


class AlternativeFinderResponse(BaseModel):
    alternatives: List[AlternativeProduct] = Field(..., description="List of safe alternative products")


class ProductAnalysisRequest(BaseModel):
    s3_image_url: str = Field(..., description="S3 URL of the product image")
    allergens: List[str] = Field(..., description="List of allergens to check/avoid")

    class Config:
        json_schema_extra = {
            "example": {
                "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
                "allergens": ["Milk", "Peanuts", "Gluten"]
            }
        }


class ProductAnalysisResponse(BaseModel):
    allergen_analysis: AllergenDetectionResponse = Field(..., description="Allergen detection results")
    alternatives: List[AlternativeProduct] = Field(..., description="Safe alternative products")
    summary: dict = Field(..., description="Analysis summary with stats")
    all_sources: Optional[List[dict]] = Field(None, description="All research sources cited")


# Helper function
def download_s3_image(s3_url: str) -> str:
    """Download image from S3 using boto3

    Args:
        s3_url: Full S3 URL (e.g., https://bucket.s3.region.amazonaws.com/key)

    Returns:
        Path to temporary file containing the downloaded image
    """
    # Parse S3 URL to extract bucket and key
    parsed_url = urlparse(s3_url)

    # Extract bucket name from hostname (e.g., "allersafe.s3.us-east-2.amazonaws.com")
    hostname_parts = parsed_url.hostname.split('.')
    bucket_name = hostname_parts[0]

    # Extract object key from path (remove leading slash)
    object_key = parsed_url.path.lstrip('/')

    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    # Download image directly from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()

    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_file.write(image_data)
    temp_file.close()

    return temp_file.name


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AllerSafe API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze_product": "/api/analyze-product (RECOMMENDED - full 8-phase analysis)",
            "detect_allergens": "/api/detect-allergens",
            "find_alternatives": "/api/find-alternatives"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "allersafe-backend"}


@app.post("/api/analyze-product", response_model=ProductAnalysisResponse)
async def analyze_product_endpoint(request: ProductAnalysisRequest):
    """
    Complete product analysis - allergen detection + safe alternatives (8-phase pipeline)

    This is the most efficient endpoint combining both allergen detection and alternative finding.
    Runs all 8 phases in optimal order:
    - Phase 1-3: Allergen detection with web research
    - Phase 4-8: Alternative finding with web research

    Args:
        request: Contains s3_image_url and list of allergens

    Returns:
        ProductAnalysisResponse with allergen analysis, alternatives, summary, and sources
    """
    local_image_path = None

    try:
        # Download image from S3
        local_image_path = download_s3_image(request.s3_image_url)

        # Run complete 8-phase analysis using orchestrator
        result = analyze_product(local_image_path, request.allergens, verbose=False)

        # Convert to response models
        allergen_analysis = AllergenDetectionResponse(**result['allergen_analysis'])
        alternatives = [AlternativeProduct(**alt) for alt in result['alternatives']]

        return ProductAnalysisResponse(
            allergen_analysis=allergen_analysis,
            alternatives=alternatives,
            summary=result['summary'],
            all_sources=result.get('all_sources', [])
        )

    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"\n{'='*80}")
        print(f"ERROR in /api/analyze-product endpoint:")
        print(f"{'='*80}")
        print(error_traceback)
        print(f"{'='*80}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing product: {str(e)}"
        )

    finally:
        # Clean up temporary file
        if local_image_path and os.path.exists(local_image_path):
            try:
                os.unlink(local_image_path)
            except Exception as e:
                print(f"Warning: Failed to delete temp file {local_image_path}: {e}")


@app.post("/api/detect-allergens", response_model=AllergenDetectionResponse)
async def detect_allergens_endpoint(request: AllergenDetectionRequest):
    """
    Detect allergens in a product image from S3

    Args:
        request: Contains s3_image_url and list of allergens to check

    Returns:
        AllergenDetectionResponse with severity, detected allergens, and warnings
    """
    local_image_path = None

    try:
        # Download image from S3
        local_image_path = download_s3_image(request.s3_image_url)

        # Detect allergens
        result = detect_allergens(local_image_path, request.allergens)

        return AllergenDetectionResponse(**result)

    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"\n{'='*80}")
        print(f"ERROR in /api/detect-allergens endpoint:")
        print(f"{'='*80}")
        print(error_traceback)
        print(f"{'='*80}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing allergen detection: {str(e)}"
        )

    finally:
        # Clean up temporary file
        if local_image_path and os.path.exists(local_image_path):
            try:
                os.unlink(local_image_path)
            except Exception as e:
                print(f"Warning: Failed to delete temp file {local_image_path}: {e}")


@app.post("/api/find-alternatives", response_model=AlternativeFinderResponse)
async def find_alternatives_endpoint(request: AlternativeFinderRequest):
    """
    Find safe alternative products for a given product image

    This endpoint runs the full 8-phase pipeline:
    - Phase 1-3: Allergen detection (provides context about original product)
    - Phase 4-8: Alternative finding (uses allergen data for better results)

    Args:
        request: Contains s3_image_url and list of allergens to avoid

    Returns:
        AlternativeFinderResponse with list of safe alternative products
    """
    local_image_path = None

    try:
        # Download image from S3
        local_image_path = download_s3_image(request.s3_image_url)

        # Step 1: Run allergen detection first (Phase 1-3)
        # This provides context about the original product
        allergen_result = detect_allergens(local_image_path, request.allergens)

        # Step 2: Find alternatives using allergen detection results (Phase 4-8)
        # Passing allergen_result enables better alternative matching
        alternatives_list = find_alternatives(
            local_image_path,
            request.allergens,
            allergen_result
        )

        # Convert to Pydantic models
        alternatives = [AlternativeProduct(**alt) for alt in alternatives_list]

        return AlternativeFinderResponse(alternatives=alternatives)

    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"\n{'='*80}")
        print(f"ERROR in /api/find-alternatives endpoint:")
        print(f"{'='*80}")
        print(error_traceback)
        print(f"{'='*80}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error finding alternative products: {str(e)}"
        )

    finally:
        # Clean up temporary file
        if local_image_path and os.path.exists(local_image_path):
            try:
                os.unlink(local_image_path)
            except Exception as e:
                print(f"Warning: Failed to delete temp file {local_image_path}: {e}")


@app.post("/api/analyze-product-stream")
async def analyze_product_stream(request: ProductAnalysisRequest):
    """
    Stream product analysis progress with real-time phase updates (SSE)

    This endpoint provides Server-Sent Events for real-time progress tracking
    through all 8 phases of analysis.

    Phases:
    1. Analyzing product image
    2. Researching ingredients online
    3. Finalizing allergen analysis
    4. Analyzing product category
    5. Finding alternative candidates
    6. Verifying allergen safety
    7. Checking pricing and availability
    8. Selecting best alternatives

    Events sent:
    - phase: Current phase number (1-8) and description
    - result: Final analysis results
    - error: Error message if analysis fails
    """
    async def event_stream():
        local_image_path = None
        progress_queue = queue.Queue()

        try:
            # Phase 0: Download image
            yield f"data: {json.dumps({'type': 'phase', 'phase': 0, 'message': 'Preparing analysis...', 'total': 8})}\n\n"
            await asyncio.sleep(0.1)

            local_image_path = download_s3_image(request.s3_image_url)

            # Progress callback that puts updates into the queue
            def progress_callback(phase: int, message: str):
                progress_queue.put({'phase': phase, 'message': message})

            # Run analysis in background thread with progress callbacks
            from concurrent.futures import ThreadPoolExecutor

            def run_analysis_with_callbacks():
                """Run analysis with real-time progress callbacks"""
                try:
                    # Run allergen detection (phases 1-3)
                    allergen_result = detect_allergens(
                        local_image_path,
                        request.allergens,
                        progress_callback=progress_callback
                    )

                    # Run alternative finding (phases 4-8)
                    alternatives = find_alternatives(
                        local_image_path,
                        request.allergens,
                        allergen_result,
                        progress_callback=progress_callback
                    )

                    return {
                        'allergen_analysis': allergen_result,
                        'alternatives': alternatives
                    }
                except Exception as e:
                    progress_queue.put({'error': str(e)})
                    raise

            # Start analysis in background
            executor = ThreadPoolExecutor(max_workers=1)
            future = executor.submit(run_analysis_with_callbacks)

            # Stream progress updates from queue
            while not future.done():
                try:
                    # Check queue for updates (non-blocking with timeout)
                    update = progress_queue.get(timeout=0.1)

                    if 'error' in update:
                        yield f"data: {json.dumps({'type': 'error', 'message': update['error']})}\n\n"
                        break
                    else:
                        # Emit phase update
                        yield f"data: {json.dumps({'type': 'phase', 'phase': update['phase'], 'message': update['message'], 'total': 8})}\n\n"
                        await asyncio.sleep(0.05)  # Small delay to prevent overwhelming client
                except queue.Empty:
                    # No update available, continue waiting
                    await asyncio.sleep(0.1)

            # Check for any remaining updates in queue
            while not progress_queue.empty():
                update = progress_queue.get_nowait()
                if 'error' not in update:
                    yield f"data: {json.dumps({'type': 'phase', 'phase': update['phase'], 'message': update['message'], 'total': 8})}\n\n"
                    await asyncio.sleep(0.05)

            # Get final results
            analysis_results = future.result()
            allergen_analysis = analysis_results['allergen_analysis']
            alternatives = analysis_results['alternatives']

            # Collect all sources and clean (removes invalid/redirect URLs)
            all_sources = allergen_analysis.get('sources', [])
            for alt in alternatives:
                all_sources.extend(alt.get('sources', []))

            # Clean and deduplicate sources
            unique_sources = clean_sources_list(all_sources)

            safe_count = sum(1 for alt in alternatives if alt.get('warning_level') == 'Safe')
            caution_count = sum(1 for alt in alternatives if alt.get('warning_level') == 'Caution')

            result = {
                'allergen_analysis': allergen_analysis,
                'alternatives': alternatives,
                'summary': {
                    'original_product': allergen_analysis.get('product_name', 'Unknown'),
                    'safety_status': allergen_analysis.get('severity', 'Unknown'),
                    'allergens_found': allergen_analysis.get('allergens_detected', []),
                    'alternatives_found': len(alternatives),
                    'safe_alternatives': safe_count,
                    'caution_alternatives': caution_count,
                    'total_sources': len(unique_sources)
                },
                'all_sources': unique_sources
            }

            # Send final result
            yield f"data: {json.dumps({'type': 'result', 'data': result})}\n\n"

        except Exception as e:
            error_msg = str(e)
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"

        finally:
            # Clean up temp file
            if local_image_path and os.path.exists(local_image_path):
                try:
                    os.unlink(local_image_path)
                except Exception as e:
                    print(f"Warning: Failed to delete temp file: {e}")

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
