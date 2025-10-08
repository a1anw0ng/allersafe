"""
FastAPI backend for AllerSafe - Food Allergy Detection Service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from allergen_detector.allergen_detector import detect_allergens
import boto3
import tempfile
import os
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
            "detect_allergens": "/api/detect-allergens"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "allersafe-backend"}


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
