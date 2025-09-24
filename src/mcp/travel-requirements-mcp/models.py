"""Pydantic models for Travel Requirements MCP Server"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class BaggageRule(BaseModel):
    """Baggage allowance and restrictions"""
    airline: str
    cabin_class: str
    route_type: str
    carry_on_weight_kg: int
    carry_on_dimensions_cm: str  # "55x40x20"
    checked_weight_kg: int
    checked_dimensions_cm: str
    additional_fees: Optional[Dict[str, float]] = None
    prohibited_items: List[str] = []
    liquid_restrictions: Dict[str, str] = {}
    
class SecurityRestriction(BaseModel):
    """Airport security restrictions for items"""
    item: str
    status: str  # "allowed", "restricted", "prohibited"
    carry_on_allowed: bool
    checked_allowed: bool
    quantity_limit: Optional[str] = None
    size_limit: Optional[str] = None
    special_instructions: Optional[str] = None
    source: str

class VisaRequirement(BaseModel):
    """Visa requirements for travel"""
    passport_country: str
    destination_country: str
    visa_required: bool
    visa_type: Optional[str] = None
    max_stay_days: Optional[int] = None
    processing_time_days: Optional[int] = None
    fee_usd: Optional[float] = None
    documents_required: List[str] = []
    special_notes: Optional[str] = None

class TravelDocument(BaseModel):
    """Required travel documents"""
    document_type: str  # "passport", "visa", "vaccination_certificate", etc.
    required: bool
    validity_months_required: Optional[int] = None
    special_requirements: Optional[str] = None

# Request models
class BaggageRulesRequest(BaseModel):
    airline: str
    cabin_class: str = "economy"
    route: str = "international"

class SecurityRestrictionsRequest(BaseModel):
    departure_country: str
    arrival_country: str
    items: List[str] = []

class VisaRequirementsRequest(BaseModel):
    passport_country: str
    destination_country: str
    trip_duration_days: int
    purpose: str = "tourism"

class TravelDocumentsRequest(BaseModel):
    destination_country: str
    passport_country: str
    departure_date: str  # YYYY-MM-DD
    return_date: Optional[str] = None