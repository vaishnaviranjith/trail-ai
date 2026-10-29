import os
import re
import json
import uuid
import time
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from models import (
    User, PreferenceProfile, Trip, POI, Hotel, FoodPlace,
    ScoredRecommendation, DailyPlan, BudgetSummary, OfflinePackage,
    Feedback, RecommendationLog,
    TripParseRequest, TripParseResponse,
    TripGenerateRequest, TripRefineRequest, TripRefineResponse
)
from recommendation_engine import RecommendationEngine
from itinerary_engine import ItineraryEngine
from budget_engine import BudgetEngine

app = FastAPI(
    title="Trail AI - Smart Trip Planner API",
    version="1.0.0",
    description="Backend service powered by IEEE research framework (Smart Trip Planner for Personalized Tourism Itineraries, DOI: 10.1109/ICUIS67429.2025.11380545)."
)

# Enable CORS for local dev and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core intelligence engines
rec_engine = RecommendationEngine()
itin_engine = ItineraryEngine()
budget_engine = BudgetEngine()

# In-memory storage for trips, feedback, and demo user state
DB_TRIPS: Dict[str, Trip] = {}
DB_FEEDBACK: List[Feedback] = []
DB_USERS: Dict[str, User] = {
    "user_demo_traveler": User(
        user_id="user_demo_traveler",
        name="Priya & Rahul",
        email="travelers@example.com",
        is_demo=True,
        profile=PreferenceProfile(
            destination="Kerala",
            duration_days=3,
            number_of_travelers=2,
            budget=15000.0,
            interests=["Waterfalls", "Trekking"],
            food_preference="Local Food",
            hotel_preference="Budget Hotel",
            travel_pace="Moderate pace",
            transport_preference="Local Taxi / Cab"
        )
    )
}

# Load seed datasets (Kerala, Goa, etc.)
SEED_DATA: Dict[str, Dict[str, Any]] = {}

def load_seed_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    if os.path.exists(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith("_seed.json"):
                dest_key = f.replace("_seed.json", "").lower()
                with open(os.path.join(data_dir, f), "r", encoding="utf-8") as fp:
                    SEED_DATA[dest_key] = json.load(fp)
        # Ensure tamilnadu points to the complete 38-district dataset if available
        if "tamilnadu_complete" in SEED_DATA:
            SEED_DATA["tamilnadu"] = SEED_DATA["tamilnadu_complete"]

load_seed_data()

# Granular District Lookup & Alias Resolution for all 38 Tamil Nadu Districts
TN_DISTRICT_MAP: Dict[str, str] = {
    "coimbatore": "Coimbatore",
    "kovai": "Coimbatore",
    "nilgiris": "Nilgiris",
    "nilgiri": "Nilgiris",
    "ooty": "Nilgiris",
    "coonoor": "Nilgiris",
    "kotagiri": "Nilgiris",
    "madurai": "Madurai",
    "dindigul": "Dindigul",
    "kodaikanal": "Dindigul",
    "kodai": "Dindigul",
    "thanjavur": "Thanjavur",
    "tanjore": "Thanjavur",
    "kumbakonam": "Thanjavur",
    "ramanathapuram": "Ramanathapuram",
    "rameswaram": "Ramanathapuram",
    "rameshwaram": "Ramanathapuram",
    "dhanushkodi": "Ramanathapuram",
    "kanyakumari": "Kanyakumari",
    "cape comorin": "Kanyakumari",
    "salem": "Salem",
    "yercaud": "Salem",
    "tiruchirappalli": "Tiruchirappalli",
    "trichy": "Tiruchirappalli",
    "srirangam": "Tiruchirappalli",
    "tirunelveli": "Tirunelveli",
    "nellai": "Tirunelveli",
    "vellore": "Vellore",
    "erode": "Erode",
    "bhavani": "Erode",
    "tiruppur": "Tiruppur",
    "tirupur": "Tiruppur",
    "karur": "Karur",
    "nagapattinam": "Nagapattinam",
    "velankanni": "Nagapattinam",
    "nagore": "Nagapattinam",
    "cuddalore": "Cuddalore",
    "pichavaram": "Cuddalore",
    "villupuram": "Villupuram",
    "gingee": "Villupuram",
    "namakkal": "Namakkal",
    "kolli": "Namakkal",
    "kolli hills": "Namakkal",
    "dharmapuri": "Dharmapuri",
    "hogenakkal": "Dharmapuri",
    "krishnagiri": "Krishnagiri",
    "hosur": "Krishnagiri",
    "theni": "Theni",
    "meghamalai": "Theni",
    "suruli": "Theni",
    "sivaganga": "Sivaganga",
    "chettinad": "Sivaganga",
    "karaikudi": "Sivaganga",
    "virudhunagar": "Virudhunagar",
    "srivilliputhur": "Virudhunagar",
    "thoothukudi": "Thoothukudi",
    "tuticorin": "Thoothukudi",
    "tiruchendur": "Thoothukudi",
    "tenkasi": "Tenkasi",
    "courtallam": "Tenkasi",
    "kutralam": "Tenkasi",
    "kallakurichi": "Kallakurichi",
    "kalvarayan": "Kallakurichi",
    "ranipet": "Ranipet",
    "arcot": "Ranipet",
    "walajah": "Ranipet",
    "tirupattur": "Tirupattur",
    "yelagiri": "Tirupattur",
    "ambur": "Tirupattur",
    "chengalpattu": "Chengalpattu",
    "mahabalipuram": "Chengalpattu",
    "mamallapuram": "Chengalpattu",
    "kanchipuram": "Kanchipuram",
    "kanchi": "Kanchipuram",
    "thiruvallur": "Thiruvallur",
    "tiruvallur": "Thiruvallur",
    "mayiladuthurai": "Mayiladuthurai",
    "tranquebar": "Mayiladuthurai",
    "tharangambadi": "Mayiladuthurai",
    "perambalur": "Perambalur",
    "ariyalur": "Ariyalur",
    "gangaikonda": "Ariyalur",
    "pudukkottai": "Pudukkottai",
    "sittanavasal": "Pudukkottai",
    "tiruvarur": "Tiruvarur",
    "thiruvarur": "Tiruvarur",
    "chennai": "Chennai",
    "madras": "Chennai",
    "tiruvannamalai": "Tiruvannamalai",
    "arunachala": "Tiruvannamalai"
}

def extract_target_districts(text: str) -> List[str]:
    """Helper to detect all district mentions in text while avoiding substrings."""
    if not text:
        return []
    t_low = text.lower()
    matched: List[str] = []
    # Sort keys by length descending to match longer multi-word phrases first
    for kw in sorted(TN_DISTRICT_MAP.keys(), key=lambda x: len(x), reverse=True):
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, t_low):
            d_name = TN_DISTRICT_MAP[kw]
            if d_name not in matched:
                matched.append(d_name)
    return matched

def get_destination_data(destination: str) -> Dict[str, Any]:
    dest_lower = (destination or "Kerala").lower().strip()
    if "tamil" in dest_lower or "tn" in dest_lower or any(kw in dest_lower for kw in TN_DISTRICT_MAP.keys()):
        return SEED_DATA.get("tamilnadu_complete", SEED_DATA.get("tamilnadu", SEED_DATA.get("kerala", {})))
    if "goa" in dest_lower:
        return SEED_DATA.get("goa", SEED_DATA.get("kerala", {}))
    # Default to Kerala
    return SEED_DATA.get("kerala", list(SEED_DATA.values())[0] if SEED_DATA else {})

# ==================== NLP PARSER ENGINE ====================

def parse_natural_language_prompt(prompt: str) -> TripParseResponse:
    """
    IEEE NLP Extraction Layer: converts unstructured travel text into
    structured profile parameters (destination, duration, budget, tier, interests, preferences)
    with full dynamic district-by-district extraction for Tamil Nadu's 38 districts.
    Example: 'Plan a 3-day Coimbatore and Ooty trip for 15,000 with Kongu food and tea plantations'
    """
    text = prompt.lower().strip()
    extracted_entities: Dict[str, Any] = {}

    # 1. District Recognition & Destination
    destination = "Kerala"
    matched_districts = extract_target_districts(text)
    is_cross_district = len(matched_districts) > 1

    if matched_districts:
        destination = "Tamil Nadu"
        extracted_entities["target_districts"] = matched_districts
        extracted_entities["is_cross_district"] = is_cross_district
        if is_cross_district:
            extracted_entities["destination"] = f"Tamil Nadu ({', '.join(matched_districts)})"
        else:
            extracted_entities["destination"] = f"Tamil Nadu ({matched_districts[0]})"
    elif "tamil nadu" in text or "tamilnadu" in text or "tn" in text:
        destination = "Tamil Nadu"
        extracted_entities["destination"] = "Tamil Nadu"
    elif "goa" in text:
        destination = "Goa"
        extracted_entities["destination"] = "Goa"
    elif "kerala" in text or "munnar" in text or "kochi" in text or "alleppey" in text or "wayanad" in text:
        destination = "Kerala"
        extracted_entities["destination"] = "Kerala"
    else:
        extracted_entities["destination_inferred"] = destination

    # 2. Duration (Days)
    duration_days = 3
    day_match = re.search(r'(\d+)\s*(?:-| )?\s*days?', text)
    if day_match:
        duration_days = int(day_match.group(1))
        extracted_entities["duration_match"] = f"{duration_days} days"
    elif "weekend" in text:
        duration_days = 2
        extracted_entities["duration_match"] = "weekend (2 days)"
    elif "week" in text:
        duration_days = 7
        extracted_entities["duration_match"] = "week (7 days)"

    duration_days = max(1, min(14, duration_days))

    # 3. Budget & Budget Tier
    budget = 15000.0
    budget_k_match = re.search(r'(\d+(?:\.\d+)?)\s*k\b', text)
    budget_match = None
    if budget_k_match:
        budget = float(budget_k_match.group(1)) * 1000.0
        extracted_entities["budget_raw"] = f"{budget_k_match.group(1)}k"
    else:
        budget_match = re.search(r'(?:₹|rs\.?|inr|for|budget\s*(?:of)?)\s*([\d,]+)', text)
        if budget_match:
            raw_val = budget_match.group(1).replace(",", "")
            if raw_val.isdigit() and int(raw_val) >= 500:
                budget = float(raw_val)
                extracted_entities["budget_raw"] = raw_val
        else:
            numbers = re.findall(r'\b\d{4,6}\b', text)
            if numbers:
                budget = float(numbers[0])
                extracted_entities["budget_raw"] = numbers[0]

    # Classify budget tier
    if budget < 16000:
        budget_tier = "Budget"
    elif budget <= 35000:
        budget_tier = "Moderate"
    else:
        budget_tier = "Luxury"

    if "luxury" in text or "resort" in text or "5 star" in text:
        budget_tier = "Luxury"
    elif "budget" in text or "cheap" in text or "backpack" in text:
        budget_tier = "Budget"

    # 4. Number of Travelers
    number_of_travelers = 2
    traveler_match = re.search(r'(\d+)\s*(?:travelers?|people|persons?|adults?)', text)
    if traveler_match:
        number_of_travelers = int(traveler_match.group(1))
    elif "solo" in text or "alone" in text:
        number_of_travelers = 1
    elif "family" in text:
        number_of_travelers = 4
    elif "couple" in text or "partner" in text:
        number_of_travelers = 2

    number_of_travelers = max(1, min(20, number_of_travelers))

    # 5. Interests
    interests = []
    interest_keywords = {
        "waterfalls": "Waterfalls",
        "waterfall": "Waterfalls",
        "falls": "Waterfalls",
        "trek": "Trekking",
        "trekking": "Trekking",
        "hike": "Trekking",
        "hiking": "Trekking",
        "beach": "Beaches",
        "beaches": "Beaches",
        "heritage": "Heritage",
        "temple": "Heritage",
        "church": "Heritage",
        "fort": "Heritage",
        "wildlife": "Wildlife",
        "sanctuary": "Wildlife",
        "nature": "Nature & Plantations",
        "tea": "Nature & Plantations",
        "viewpoint": "Nature & Plantations",
        "adventure": "Adventure",
        "watersports": "Adventure",
        "food": "Food & Dining"
    }
    for kw, label in interest_keywords.items():
        if kw in text and label not in interests:
            interests.append(label)

    if not interests:
        if matched_districts:
            highland_districts = {"Nilgiris", "Dindigul", "Salem", "Namakkal", "Theni", "Tirupattur", "Tenkasi"}
            heritage_districts = {"Madurai", "Thanjavur", "Kanchipuram", "Tiruchirappalli", "Pudukkottai", "Sivaganga"}
            coastal_districts = {"Ramanathapuram", "Kanyakumari", "Thoothukudi", "Nagapattinam", "Chengalpattu", "Chennai"}
            
            if any(d in highland_districts for d in matched_districts):
                interests.append("Nature & Plantations")
                interests.append("Waterfalls")
            if any(d in heritage_districts for d in matched_districts):
                interests.append("Heritage")
            if any(d in coastal_districts for d in matched_districts):
                interests.append("Beaches")
            if not interests:
                interests = ["Heritage", "Nature & Plantations"]
        elif destination == "Goa":
            interests = ["Beaches", "Waterfalls"]
        elif destination == "Tamil Nadu":
            interests = ["Heritage", "Nature & Plantations"]
        else:
            interests = ["Waterfalls", "Trekking"]

    # 6. Food Preference
    food_preference = "Local Food"
    if "seafood" in text:
        food_preference = "Seafood Specialties"
    elif "chettinad" in text or "Sivaganga" in matched_districts:
        food_preference = "Chettinad Spicy Traditional"
    elif "kongu" in text or "Coimbatore" in matched_districts or "Erode" in matched_districts:
        food_preference = "Kongu Nadu Traditional"
    elif "jigarthanda" in text or "Madurai" in matched_districts:
        food_preference = "Madurai Traditional & Tiffin"
    elif "varkey" in text or "Nilgiris" in matched_districts:
        food_preference = "Nilgiri Highland Tea & Bakes"
    elif "veg" in text or "vegetarian" in text or "idli" in text or "dosa" in text:
        food_preference = "Pure Vegetarian"
    elif "local" in text or "authentic" in text or "kerala food" in text or "tamil food" in text:
        food_preference = "Local Food"

    # 7. Hotel Preference
    hotel_preference = "Budget Hotel"
    if budget_tier == "Luxury" or "resort" in text:
        hotel_preference = "Luxury Resort"
    elif "homestay" in text:
        hotel_preference = "Homestay"
    elif "hostel" in text:
        hotel_preference = "Backpacker Hostel"

    # 8. Travel Pace
    travel_pace = "Moderate pace"
    if "relaxed" in text or "slow" in text or "leisure" in text:
        travel_pace = "Relaxed pace"
    elif "fast" in text or "quick" in text or "packed" in text:
        travel_pace = "Fast pace"

    # 9. Transport Preference
    transport_preference = "Local Taxi / Cab"
    if "bike" in text or "scooter" in text:
        transport_preference = "Self-drive Scooter / Bike"
    elif "bus" in text or "public" in text:
        transport_preference = "Public Transit"

    confidence = 0.94 if (day_match and (budget_match or budget_k_match)) else 0.88

    return TripParseResponse(
        destination=destination,
        duration_days=duration_days,
        budget=budget,
        budget_tier=budget_tier,
        number_of_travelers=number_of_travelers,
        interests=interests,
        food_preference=food_preference,
        hotel_preference=hotel_preference,
        travel_pace=travel_pace,
        transport_preference=transport_preference,
        confidence=confidence,
        extracted_entities=extracted_entities,
        extracted_districts=matched_districts,
        is_cross_district=is_cross_district
    )

# ==================== CORE REQUIRED ENDPOINTS ====================

@app.post("/trip/parse", response_model=TripParseResponse)
def parse_trip(request: TripParseRequest):
    """
    Extracts structured trip parameters from unstructured user natural-language input.
    """
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt must not be empty.")
    return parse_natural_language_prompt(request.prompt)

@app.post("/trip/generate", response_model=Trip)
def generate_trip(request: TripGenerateRequest):
    """
    Orchestrates candidate retrieval, recommendation scoring, route sequencing,
    and budget estimation to output a complete, production-ready itinerary
    with dynamic district-by-district accuracy and mountain transit support.
    """
    start_time = time.time()

    # Determine profile from prompt or direct profile object
    if request.profile:
        profile = request.profile
    elif request.prompt:
        parsed = parse_natural_language_prompt(request.prompt)
        profile = PreferenceProfile(
            destination=parsed.destination,
            duration_days=parsed.duration_days,
            number_of_travelers=parsed.number_of_travelers,
            budget=parsed.budget,
            interests=parsed.interests,
            food_preference=parsed.food_preference,
            hotel_preference=parsed.hotel_preference,
            travel_pace=parsed.travel_pace,
            transport_preference=parsed.transport_preference,
            free_text_request=request.prompt
        )
    else:
        profile = PreferenceProfile()

    trip_id = f"trip_{uuid.uuid4().hex[:10]}"
    dest_data = get_destination_data(profile.destination)

    # Granular district discovery
    target_districts = extract_target_districts(
        f"{request.prompt or ''} {profile.free_text_request or ''} {profile.destination or ''}"
    )

    district_profiles = dest_data.get("districts", {})
    district_anchors = {d_id: d.get("center_coordinates", {}) for d_id, d in district_profiles.items()}

    # Anchor selection: set to primary requested district center if available
    anchor = dest_data.get("center_coordinates", {"lat": 10.0889, "lng": 77.0595})
    if target_districts:
        primary_d_key = target_districts[0].lower().strip()
        if primary_d_key in district_profiles:
            anchor = district_profiles[primary_d_key].get("center_coordinates", anchor)

    raw_pois = [POI(**p) for p in dest_data.get("pois", [])]
    raw_hotels = [Hotel(**h) for h in dest_data.get("hotels", [])]
    raw_foods = [FoodPlace(**f) for f in dest_data.get("food_places", [])]

    # 1. Recommendation scoring with target district weighting
    ranked_tuples = rec_engine.rank_pois(
        raw_pois, profile, anchor["lat"], anchor["lng"],
        target_districts=target_districts,
        district_anchors=district_anchors
    )
    scored_recs = [t[1] for t in ranked_tuples]

    # 2. Basecamp Hotel & Dining selections
    selected_hotel = rec_engine.select_best_hotel(
        raw_hotels, profile, anchor["lat"], anchor["lng"],
        target_districts=target_districts
    )
    selected_foods = rec_engine.select_food_places(
        raw_foods, profile, count=4,
        target_districts=target_districts
    )

    # 3. Constraint-satisfaction route & clustering engine
    daily_plans = itin_engine.build_daily_plans(
        ranked_tuples, selected_hotel, selected_foods, profile,
        target_districts=target_districts,
        district_profiles=district_profiles
    )

    # 4. Dynamic predictive budget engine
    budget_summary = budget_engine.compute_budget_summary(profile, selected_hotel, daily_plans)

    # 5. Build Offline Package
    now_str = datetime.now(timezone.utc).isoformat()
    offline_pkg = OfflinePackage(
        trip_id=trip_id,
        destination=profile.destination,
        generated_at=now_str,
        expires_at=now_str,
        travelers_count=profile.number_of_travelers,
        total_budget=profile.budget,
        daily_plans=daily_plans,
        hotel_details=selected_hotel,
        food_recommendations=selected_foods,
        budget_summary=budget_summary,
        emergency_contacts=dest_data.get("emergency_contacts", []),
        offline_instructions=f"Locally cached offline pack for {profile.destination}. Timings, venue details, and safety helplines remain active without internet."
    )

    trip = Trip(
        trip_id=trip_id,
        user_id=request.user_id or "user_demo_traveler",
        status="planned",
        profile=profile,
        recommendations=scored_recs,
        daily_plans=daily_plans,
        selected_hotel=selected_hotel,
        selected_food_places=selected_foods,
        budget_summary=budget_summary,
        offline_package=offline_pkg,
        created_at=now_str,
        updated_at=now_str
    )

    DB_TRIPS[trip_id] = trip
    return trip

@app.post("/trip/refine", response_model=TripRefineResponse)
def refine_trip(req: TripRefineRequest):
    """
    Adjusts specific itinerary segments based on user modifications:
    - swap_hotel: re-anchors transit routes and recalculates stay budget
    - remove_poi: deletes stop and smoothly recalibrates day timeline
    - add_poi: inserts candidate POI into selected day slot
    - swap_poi: replaces an existing POI with an alternative
    - update_constraints: modifies pace, transport, or budget ceiling
    """
    if req.trip_id not in DB_TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip = DB_TRIPS[req.trip_id]
    dest_data = get_destination_data(trip.profile.destination)
    anchor = dest_data.get("center_coordinates", {"lat": 10.0889, "lng": 77.0595})
    all_pois = [POI(**p) for p in dest_data.get("pois", [])]
    all_hotels = [Hotel(**h) for h in dest_data.get("hotels", [])]

    district_profiles = dest_data.get("districts", {})
    district_anchors = {d_id: d.get("center_coordinates", {}) for d_id, d in district_profiles.items()}
    t_districts = extract_target_districts(f"{trip.profile.free_text_request or ''} {trip.profile.destination or ''}")

    msg = "Itinerary refined successfully"

    if req.action == "swap_hotel" and req.hotel_id:
        chosen = next((h for h in all_hotels if h.id == req.hotel_id), None)
        if not chosen:
            raise HTTPException(status_code=404, detail="Requested hotel not found")
        trip.selected_hotel = chosen
        # Re-anchor first day checkin and transit
        if trip.daily_plans:
            raw_pois = [POI(**p) for p in dest_data.get("pois", [])]
            ranked_tuples = rec_engine.rank_pois(
                raw_pois, trip.profile, chosen.lat, chosen.lng,
                target_districts=t_districts,
                district_anchors=district_anchors
            )
            trip.daily_plans = itin_engine.build_daily_plans(
                ranked_tuples, chosen, trip.selected_food_places, trip.profile,
                target_districts=t_districts,
                district_profiles=district_profiles
            )
        msg = f"Hotel swapped to {chosen.name}. Routes and accommodation budget updated."

    elif req.action == "remove_poi" and req.poi_id:
        day_num = req.day_number or 1
        trip.daily_plans = itin_engine.remove_poi_from_day(trip.daily_plans, day_num, req.poi_id, trip.profile)
        msg = f"Removed POI from Day {day_num} schedule."

    elif req.action == "add_poi" and req.target_poi_id:
        chosen_poi = next((p for p in all_pois if p.id == req.target_poi_id), None)
        if not chosen_poi:
            raise HTTPException(status_code=404, detail="Target POI not found")
        day_num = req.day_number or 1
        slot = req.slot or "afternoon"
        trip.daily_plans = itin_engine.add_poi_to_day(trip.daily_plans, day_num, chosen_poi, slot, trip.profile)
        msg = f"Added {chosen_poi.name} to Day {day_num} ({slot})."

    elif req.action == "swap_poi" and req.poi_id and req.target_poi_id:
        chosen_poi = next((p for p in all_pois if p.id == req.target_poi_id), None)
        if not chosen_poi:
            raise HTTPException(status_code=404, detail="Target replacement POI not found")
        day_num = req.day_number or 1
        trip.daily_plans = itin_engine.swap_poi_in_day(trip.daily_plans, day_num, req.poi_id, chosen_poi, trip.profile)
        msg = f"Swapped stop with {chosen_poi.name} on Day {day_num}."

    elif req.action == "update_constraints" and req.profile_updates:
        for k, v in req.profile_updates.items():
            if hasattr(trip.profile, k):
                setattr(trip.profile, k, v)
        msg = "Trip constraints updated."

    # Always recompute budget summary after refinement
    if trip.selected_hotel:
        trip.budget_summary = budget_engine.compute_budget_summary(trip.profile, trip.selected_hotel, trip.daily_plans)
        if trip.offline_package:
            trip.offline_package.daily_plans = trip.daily_plans
            trip.offline_package.hotel_details = trip.selected_hotel
            trip.offline_package.budget_summary = trip.budget_summary

    trip.updated_at = datetime.now(timezone.utc).isoformat()
    return TripRefineResponse(
        success=True,
        action=req.action,
        message=msg,
        trip=trip
    )

@app.get("/districts")
def list_all_districts():
    """Returns the complete registry of all 38 Tamil Nadu districts with metadata, specialties, and coordinates."""
    dest_data = get_destination_data("Tamil Nadu")
    districts = dest_data.get("districts", {})
    return [
        {
            "district_id": d["district_id"],
            "name": d["name"],
            "region": d["region"],
            "headquarters": d["headquarters"],
            "center_coordinates": d["center_coordinates"],
            "is_ghat_region": d.get("is_ghat_region", False),
            "food_specialties": d.get("food_specialties", []),
            "description": d.get("description", ""),
            "poi_count": len(d.get("pois", [])),
            "hotel_count": len(d.get("hotels", [])),
            "food_count": len(d.get("food_places", []))
        }
        for d in districts.values()
    ]

@app.get("/districts/{district_id}")
def get_district_profile(district_id: str):
    """Retrieve deep profile for a single district including its POIs, stay, and food."""
    dest_data = get_destination_data("Tamil Nadu")
    districts = dest_data.get("districts", {})
    d_norm = district_id.lower().strip()
    if d_norm in districts:
        return districts[d_norm]
    # Check aliases
    for d in districts.values():
        if d_norm in [a.lower() for a in d.get("alias_names", [])]:
            return d
    raise HTTPException(status_code=404, detail=f"District '{district_id}' not found.")

@app.get("/pois", response_model=List[POI])
def list_pois(
    destination: str = "Kerala",
    district: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_price: Optional[float] = None
):
    """
    Retrieves available candidate points-of-interest filtered by destination, district, and category.
    """
    dest_str = destination if isinstance(destination, str) else "Kerala"
    dest_data = get_destination_data(dest_str)
    pois = [POI(**p) for p in dest_data.get("pois", [])]

    if district:
        d_norm = district.lower().strip()
        pois = [p for p in pois if p.district and p.district.lower().strip() == d_norm]

    if category and isinstance(category, str):
        cat_low = category.lower()
        pois = [p for p in pois if cat_low in p.category.lower()]

    if search and isinstance(search, str):
        s_low = search.lower()
        pois = [
            p for p in pois
            if s_low in p.name.lower() or s_low in p.description.lower() or any(s_low in t.lower() for t in p.tags)
        ]

    if min_rating is not None and isinstance(min_rating, (int, float)):
        pois = [p for p in pois if p.rating >= min_rating]

    if max_price is not None and isinstance(max_price, (int, float)):
        pois = [p for p in pois if p.entry_fee_per_person <= max_price]

    return pois


@app.get("/budget", response_model=BudgetSummary)
def get_budget_breakdown(
    trip_id: Optional[str] = Query(None, description="Trip ID to retrieve cached budget for"),
    destination: str = Query("Kerala", description="Target destination if computing on the fly"),
    duration_days: int = Query(3, ge=1, le=14),
    travelers: int = Query(2, ge=1, le=20),
    budget: float = Query(15000.0, ge=1000.0),
    hotel_category: str = Query("Budget Hotel")
):
    """
    Returns the category-wise expenditure breakdown (accommodation, food, activities, transit, buffer).
    """
    if trip_id:
        if trip_id in DB_TRIPS and DB_TRIPS[trip_id].budget_summary:
            return DB_TRIPS[trip_id].budget_summary
        raise HTTPException(status_code=404, detail="Trip or budget summary not found")

    # On-the-fly budget computation
    profile = PreferenceProfile(
        destination=destination,
        duration_days=duration_days,
        number_of_travelers=travelers,
        budget=budget,
        hotel_preference=hotel_category
    )
    dest_data = get_destination_data(destination)
    anchor = dest_data.get("center_coordinates", {"lat": 10.0889, "lng": 77.0595})
    raw_hotels = [Hotel(**h) for h in dest_data.get("hotels", [])]
    hotel = rec_engine.select_best_hotel(raw_hotels, profile, anchor["lat"], anchor["lng"])
    
    return budget_engine.compute_budget_summary(profile, hotel, [])

# ==================== BACKWARD COMPATIBLE & DEMO ROUTES ====================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Trail AI Smart Trip Planner API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "destinations_available": list(SEED_DATA.keys()),
        "architecture": "IEEE 2025/2026 Modular Hybrid Recommender + Constraint Solver"
    }

@app.get("/evaluation/results")
def get_evaluation_results():
    eval_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evaluation", "evaluation_results.json")
    if os.path.exists(eval_file):
        with open(eval_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"status": "ready", "message": "Evaluation test harness available."}

@app.post("/auth/profile", response_model=User)
def create_or_update_profile(user_data: User):
    DB_USERS[user_data.user_id] = user_data
    return user_data

@app.get("/auth/demo-user", response_model=User)
def get_demo_user():
    return DB_USERS["user_demo_traveler"]

@app.post("/trips", response_model=Trip)
def create_trip(profile: PreferenceProfile, user_id: str = "user_demo_traveler"):
    trip_id = f"trip_{uuid.uuid4().hex[:10]}"
    now_str = datetime.now(timezone.utc).isoformat()
    new_trip = Trip(
        trip_id=trip_id,
        user_id=user_id,
        status="draft",
        profile=profile,
        created_at=now_str,
        updated_at=now_str
    )
    DB_TRIPS[trip_id] = new_trip
    return new_trip

@app.post("/trips/{trip_id}/plan", response_model=Trip)
def generate_trip_plan(trip_id: str, profile_override: Optional[PreferenceProfile] = None):
    # Delegate to generate_trip logic
    req = TripGenerateRequest(profile=profile_override)
    trip = generate_trip(req)
    # Reassign requested trip_id
    if trip_id in DB_TRIPS:
        del DB_TRIPS[trip_id]
    trip.trip_id = trip_id
    DB_TRIPS[trip_id] = trip
    return trip

@app.get("/trips/{trip_id}", response_model=Trip)
def get_trip(trip_id: str):
    if trip_id not in DB_TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    return DB_TRIPS[trip_id]

@app.get("/trips", response_model=List[Trip])
def list_trips(user_id: Optional[str] = None):
    if user_id:
        return [t for t in DB_TRIPS.values() if t.user_id == user_id]
    return list(DB_TRIPS.values())

@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: str):
    if trip_id in DB_TRIPS:
        del DB_TRIPS[trip_id]
        return {"success": True, "message": "Trip deleted successfully"}
    raise HTTPException(status_code=404, detail="Trip not found")

@app.get("/trips/{trip_id}/recommendations", response_model=List[ScoredRecommendation])
def get_trip_recommendations(trip_id: str):
    if trip_id not in DB_TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    return DB_TRIPS[trip_id].recommendations

@app.get("/trips/{trip_id}/itinerary", response_model=List[DailyPlan])
def get_trip_itinerary(trip_id: str):
    if trip_id not in DB_TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    return DB_TRIPS[trip_id].daily_plans

@app.get("/trips/{trip_id}/budget", response_model=BudgetSummary)
def get_trip_budget(trip_id: str):
    if trip_id not in DB_TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    if not DB_TRIPS[trip_id].budget_summary:
        raise HTTPException(status_code=400, detail="Budget not yet calculated")
    return DB_TRIPS[trip_id].budget_summary

@app.post("/trips/{trip_id}/offline-package", response_model=OfflinePackage)
def get_or_create_offline_package(trip_id: str):
    if trip_id not in DB_TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    trip = DB_TRIPS[trip_id]
    if not trip.offline_package:
        raise HTTPException(status_code=400, detail="Trip plan not yet generated")
    return trip.offline_package

@app.post("/trips/{trip_id}/feedback")
def submit_feedback(trip_id: str, feedback: Feedback):
    feedback.trip_id = trip_id
    DB_FEEDBACK.append(feedback)
    return {"success": True, "message": "Feedback recorded", "feedback": feedback}

@app.get("/destinations/{destination}/hotels", response_model=List[Hotel])
def get_destination_hotels(destination: str):
    dest_data = get_destination_data(destination)
    return [Hotel(**h) for h in dest_data.get("hotels", [])]

@app.post("/trips/{trip_id}/select-hotel", response_model=Trip)
def select_trip_hotel(trip_id: str, hotel_id: str = Body(..., embed=True)):
    refine_res = refine_trip(TripRefineRequest(trip_id=trip_id, action="swap_hotel", hotel_id=hotel_id))
    return refine_res.trip

@app.get("/places/search")
def search_places(query: str = Query(..., min_length=2), destination: str = "Kerala"):
    dest_data = get_destination_data(destination)
    q_low = query.lower()
    pois = [p for p in dest_data.get("pois", []) if q_low in p["name"].lower() or q_low in p["category"].lower()]
    hotels = [h for h in dest_data.get("hotels", []) if q_low in h["name"].lower()]
    foods = [f for f in dest_data.get("food_places", []) if q_low in f["name"].lower() or q_low in f["cuisine"].lower()]
    return {
        "query": query,
        "destination": destination,
        "results": {
            "pois": pois,
            "hotels": hotels,
            "food_places": foods
        }
    }

# ==================== STATIC FILE SERVING ====================

# Mount production Vite dist if present, else fallback to public
dist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public")

if os.path.exists(dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_dir, "assets")), name="assets")
elif os.path.exists(public_dir):
    app.mount("/static", StaticFiles(directory=public_dir), name="static")

@app.get("/")
def serve_root():
    if os.path.exists(dist_dir):
        index_file = os.path.join(dist_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
    if os.path.exists(public_dir):
        index_file = os.path.join(public_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
    return {
        "message": "Trail AI API Running. Build frontend to access UI at root.",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
