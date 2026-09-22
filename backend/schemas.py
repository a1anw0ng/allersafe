"""Pydantic schemas for LLM phase outputs.

Every phase in the 8-step pipeline returns JSON parsed via
`Model.model_validate_json(...)` — if Claude's output doesn't match the
schema, we get a structured ValidationError and fall back to a safe
default rather than passing malformed data downstream.

Fields with `Optional` may be missing. Fields with defaults are filled in
when absent. `Literal` enforces the allowed values for enums (severity,
safety_status, etc.).
"""

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class SourceCitation(BaseModel):
    """A single web source cited by the model."""
    model_config = ConfigDict(extra="allow")  # accept extra fields like 'relevance'
    title: str = ""
    url: str


# ─────────────────────────────────────────────────────────────
# Phase 1 — Image analysis (no web search)
# ─────────────────────────────────────────────────────────────

class Phase1Output(BaseModel):
    """Output of visual analysis. is_product=False means no product in image."""
    model_config = ConfigDict(extra="allow")
    is_product: bool = True
    product_name: Optional[str] = None
    brand: Optional[str] = None
    product_type: Optional[str] = None
    # Claude may return a list of ingredients OR a status string like "not_visible"
    visible_ingredients: Union[List[str], str] = "not_visible"
    visible_allergen_warnings: List[str] = Field(default_factory=list)
    ingredient_list_status: Optional[str] = None
    needs_research: bool = True
    research_needed_for: List[str] = Field(default_factory=list)
    description: Optional[str] = None  # populated when is_product=False


# ─────────────────────────────────────────────────────────────
# Phase 2 — Web research (RAG)
# ─────────────────────────────────────────────────────────────

class Phase2Output(BaseModel):
    """Output of web-verified ingredient research."""
    model_config = ConfigDict(extra="allow")
    complete_ingredients: Union[List[str], str] = "not_found"
    allergen_warnings_found: List[str] = Field(default_factory=list)
    cross_contamination_risks: List[str] = Field(default_factory=list)
    recalls_or_advisories: List[str] = Field(default_factory=list)
    sources: List[SourceCitation] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Phase 3 — Final allergen assessment
# ─────────────────────────────────────────────────────────────

class Phase3Output(BaseModel):
    """Structured verdict for a scanned product."""
    model_config = ConfigDict(extra="allow")
    severity: Literal["Safe", "Caution", "Dangerous", "NotDetected"]
    allergens_detected: List[str] = Field(default_factory=list)
    warnings: str = ""
    product_name: Optional[str] = None
    sources: List[SourceCitation] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Phase 4 — Product categorization
# ─────────────────────────────────────────────────────────────

class OriginalProduct(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str = ""
    category: str = ""
    type: str = ""
    characteristics: List[str] = Field(default_factory=list)


class AllergenConstraints(BaseModel):
    model_config = ConfigDict(extra="allow")
    must_avoid_ingredients: List[str] = Field(default_factory=list)
    must_avoid_warnings: List[str] = Field(default_factory=list)
    acceptable_if: List[str] = Field(default_factory=list)


class SearchStrategy(BaseModel):
    model_config = ConfigDict(extra="allow")
    product_categories_to_search: List[str] = Field(default_factory=list)
    known_safe_brands: List[str] = Field(default_factory=list)
    search_terms: List[str] = Field(default_factory=list)
    dietary_certifications: List[str] = Field(default_factory=list)


class Phase4Output(BaseModel):
    """Category analysis output that drives phases 5-8."""
    model_config = ConfigDict(extra="allow")
    original_product: OriginalProduct = Field(default_factory=OriginalProduct)
    allergen_constraints: AllergenConstraints = Field(default_factory=AllergenConstraints)
    search_strategy: SearchStrategy = Field(default_factory=SearchStrategy)
    priority_guidance: str = ""


# ─────────────────────────────────────────────────────────────
# Phase 5 — Candidate alternatives (RAG)
# ─────────────────────────────────────────────────────────────

class Candidate(BaseModel):
    model_config = ConfigDict(extra="allow")
    product_name: str = ""
    company: str = ""
    product_type: str = ""
    key_features: List[str] = Field(default_factory=list)


class Phase5Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    candidates: List[Candidate] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Phase 6 — Safety verification per candidate (RAG)
# ─────────────────────────────────────────────────────────────

class SafetyResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    product_name: str = ""
    safety_status: Literal["Safe", "Caution", "Dangerous", "Unknown"] = "Unknown"
    ingredients_found: Union[List[str], str] = "not_found"
    allergen_warnings: List[str] = Field(default_factory=list)
    contains_user_allergens: List[str] = Field(default_factory=list)
    cross_contamination_risk: Literal["none", "low", "medium", "high"] = "high"
    certifications: List[str] = Field(default_factory=list)
    safety_explanation: str = ""


class Phase6Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    safety_results: List[SafetyResult] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Phase 7 — Pricing & availability (RAG)
# ─────────────────────────────────────────────────────────────

class PricingResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    product_name: str = ""
    price: str = "N/A"
    availability: str = ""


class Phase7Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    pricing_results: List[PricingResult] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Phase 8 — Final ranked alternatives
# ─────────────────────────────────────────────────────────────

class FinalAlternative(BaseModel):
    """One product in the final ranked list returned to the frontend."""
    model_config = ConfigDict(extra="allow")
    alternative_name: str = ""
    company: str = ""
    purchase_links: List[str] = Field(default_factory=list)
    price: str = "N/A"
    warning_level: Literal["Safe", "Caution", "Dangerous"] = "Caution"
    tags: List[str] = Field(default_factory=list)
    reasoning: str = ""
