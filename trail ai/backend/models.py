from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LatLng(BaseModel):
    lat: float
    lng: float

class PreferenceProfile(BaseModel):
    destination: str = "Kerala"
    duration_days: int = Field(default=3, ge=1, le=14)
    number_of_travelers: int = Field(default=2, ge=1, le=20)
    budget: float = Field(default=15000.0, ge=1000.0)
    currency: str = "INR"
    interests: List[str] = Field(default_factory=lambda: ["Waterfalls", "Trekking"])
    disliked_categories: List[str] = Field(default_factory=list)
    travel_pace: str = "Moderate pace"  # Relaxed pace, Moderate pace, Fast pace
    food_preference: str = "Local Food"
    hotel_preference: str = "Budget Hotel"
    transport_preference: str = "Local Taxi / Cab"
    max_daily_travel_hours: float = 4.0
    accessibility_requirements: Optional[str] = None
    free_text_request: Optional[str] = None

class User(BaseModel):
    user_id: str
    name: str
    email: str
    is_demo: bool = True
    profile: Optional[PreferenceProfile] = None

class POI(BaseModel):
    id: str
    name: str
    category: str
    tags: List[str] = []
    lat: float
    lng: float
    rating: float
    review_count: int
    entry_fee_per_person: float
    typical_duration_minutes: int
    opening_time: str
    closing_time: str
    description: str
    best_time_to_visit: Optional[str] = None
    difficulty: Optional[str] = None
    district: Optional[str] = None
    elevation_m: Optional[int] = None
    is_mountain_route: Optional[bool] = False

class Hotel(BaseModel):
    id: str
    name: str
    category: str
    price_per_night: float
    rating: float
    review_count: int
    lat: float
    lng: float
    address: str
    amenities: List[str] = []
    room_type: str
    description: str
    district: Optional[str] = None

class FoodPlace(BaseModel):
    id: str
    name: str
    category: str
    cuisine: str
    specialties: List[str] = []
    cost_for_two: float
    rating: float
    review_count: int
    lat: float
    lng: float
    opening_time: str
    closing_time: str
    description: str
    district: Optional[str] = None

class RouteSegment(BaseModel):
    from_name: str
    to_name: str
    distance_km: float
    travel_time_minutes: int
    transport_mode: str
    scenic_note: Optional[str] = None
    is_ghat_route: Optional[bool] = False
    buffer_minutes: Optional[int] = 0
    hairpin_bends: Optional[int] = 0
    corridor_name: Optional[str] = None

class ItineraryStop(BaseModel):
    stop_id: str
    type: str  # "poi", "hotel_checkin", "food_lunch", "food_dinner"
    name: str
    category: str
    start_time: str
    end_time: str
    duration_minutes: int
    cost_for_group: float
    lat: float
    lng: float
    description: str
    recommendation_reason: str
    tags: List[str] = []
    district: Optional[str] = None
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    food_specialties: Optional[List[str]] = None
    district_description: Optional[str] = None

class DailyPlan(BaseModel):
    day_number: int
    date_label: str
    title: str
    theme: str
    stops: List[ItineraryStop]
    route_segments: List[RouteSegment]
    total_travel_time_minutes: int
    total_distance_km: float
    day_cost: float
    is_feasible: bool = True
    feasibility_notes: List[str] = []

class BudgetItem(BaseModel):
    category: str
    label: str
    min_cost: float
    expected_cost: float
    max_cost: float
    details: str
    is_live_price: bool = False
    price_source: str = "Regional Benchmark"

class BudgetSummary(BaseModel):
    total_budget: float
    total_expected_cost: float
    min_cost: float
    max_cost: float
    currency: str = "INR"
    within_budget: bool
    budget_remaining: float
    budget_variance_percentage: float
    items: List[BudgetItem]
    warnings: List[str] = []

class RecommendationScoreBreakdown(BaseModel):
    preference_match: float
    context_match: float
    distance_score: float
    quality_score: float
    budget_fit: float
    schedule_fit: float
    total_score: float

class ScoredRecommendation(BaseModel):
    item_id: str
    name: str
    category: str
    scores: RecommendationScoreBreakdown
    primary_explanation: str
    tags: List[str]

class OfflinePackage(BaseModel):
    trip_id: str
    destination: str
    generated_at: str
    expires_at: str
    travelers_count: int
    total_budget: float
    daily_plans: List[DailyPlan]
    hotel_details: Hotel
    food_recommendations: List[FoodPlace]
    budget_summary: BudgetSummary
    emergency_contacts: List[Dict[str, str]]
    offline_instructions: str
    is_offline_ready: bool = True

class Feedback(BaseModel):
    feedback_id: Optional[str] = None
    trip_id: str
    user_id: str
    rating: int  # 1 to 5
    helpful: bool
    comment: Optional[str] = None
    liked_stops: List[str] = []

class RecommendationLog(BaseModel):
    trip_id: str
    timestamp: str
    engine_version: str = "IEEE-2025-2026-Modular-Hybrid-v1"
    top_poi_ids: List[str]
    weights_used: Dict[str, float]
    execution_time_ms: float

class Trip(BaseModel):
    trip_id: str
    user_id: str
    status: str = "active"  # "draft", "planned", "saved", "completed"
    profile: PreferenceProfile
    recommendations: List[ScoredRecommendation] = []
    daily_plans: List[DailyPlan] = []
    selected_hotel: Optional[Hotel] = None
    selected_food_places: List[FoodPlace] = []
    budget_summary: Optional[BudgetSummary] = None
    offline_package: Optional[OfflinePackage] = None
    created_at: str
    updated_at: str

class TripParseRequest(BaseModel):
    prompt: str

class TripParseResponse(BaseModel):
    destination: str
    duration_days: int
    budget: float
    budget_tier: str
    number_of_travelers: int
    interests: List[str]
    food_preference: str
    hotel_preference: str
    travel_pace: str
    transport_preference: str
    confidence: float
    extracted_entities: Dict[str, Any]
    extracted_districts: List[str] = []
    is_cross_district: bool = False

class TripGenerateRequest(BaseModel):
    prompt: Optional[str] = None
    profile: Optional[PreferenceProfile] = None
    user_id: Optional[str] = "user_demo_traveler"

class TripRefineRequest(BaseModel):
    trip_id: str
    action: str  # "swap_hotel", "remove_poi", "add_poi", "swap_poi", "update_constraints"
    hotel_id: Optional[str] = None
    poi_id: Optional[str] = None
    target_poi_id: Optional[str] = None
    day_number: Optional[int] = None
    slot: Optional[str] = None  # "morning", "afternoon", "evening"
    profile_updates: Optional[Dict[str, Any]] = None

class TripRefineResponse(BaseModel):
    success: bool
    action: str
    message: str
    trip: Trip

