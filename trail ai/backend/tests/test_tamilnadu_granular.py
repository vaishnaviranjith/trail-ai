import pytest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import TripGenerateRequest, PreferenceProfile
from main import (
    parse_natural_language_prompt, generate_trip, list_all_districts,
    get_district_profile, get_destination_data
)
from itinerary_engine import ItineraryEngine
from recommendation_engine import RecommendationEngine

def test_all_38_districts_loaded():
    """Verify all 38 districts of Tamil Nadu are fully populated with metadata and specialties."""
    districts = list_all_districts()
    assert len(districts) == 38, f"Expected 38 districts, got {len(districts)}"
    
    district_ids = {d["district_id"] for d in districts}
    expected_sample = {
        "chennai", "coimbatore", "madurai", "nilgiris", "dindigul", "thanjavur",
        "ramanathapuram", "kanyakumari", "salem", "tiruchirappalli", "tirunelveli",
        "vellore", "erode", "tiruppur", "karur", "nagapattinam", "cuddalore",
        "villupuram", "namakkal", "dharmapuri", "krishnagiri", "theni", "sivaganga",
        "virudhunagar", "thoothukudi", "tenkasi", "kallakurichi", "ranipet",
        "tirupattur", "chengalpattu", "kanchipuram", "thiruvallur", "mayiladuthurai",
        "perambalur", "ariyalur", "pudukkottai", "tiruvarur", "tiruvannamalai"
    }
    missing = expected_sample - district_ids
    assert not missing, f"Missing districts: {missing}"

    # Verify every district has coordinates and food specialties
    for d in districts:
        coords = d["center_coordinates"]
        assert "lat" in coords and "lng" in coords, f"District {d['name']} missing center coords"
        assert len(d["food_specialties"]) > 0, f"District {d['name']} missing food specialties"

def test_nlp_district_extraction_single():
    """Test NLP parser extracts single district without generic clumping."""
    res = parse_natural_language_prompt("Plan a 3-day trip to Coimbatore for 12k with Kongu food")
    assert res.destination == "Tamil Nadu"
    assert "Coimbatore" in res.extracted_districts
    assert res.is_cross_district is False
    assert res.food_preference == "Kongu Nadu Traditional"

def test_nlp_cross_district_extraction():
    """Test NLP parser extracts multiple districts for cross-district routing."""
    res = parse_natural_language_prompt("Coimbatore and Ooty trip for 18000 with tea plantations")
    assert res.destination == "Tamil Nadu"
    assert "Coimbatore" in res.extracted_districts
    assert "Nilgiris" in res.extracted_districts
    assert res.is_cross_district is True

    res2 = parse_natural_language_prompt("4 days Madurai and Rameswaram pilgrimage for 20k with seafood")
    assert "Madurai" in res2.extracted_districts
    assert "Ramanathapuram" in res2.extracted_districts
    assert res2.is_cross_district is True

def test_mountain_ghat_transit_calculation():
    """Test that mountain ghat passes accurately calculate ~24-28 km/h speeds and hairpin buffers."""
    itin = ItineraryEngine()
    
    # Check ghat location detection
    assert itin.is_ghat_location("Doddabetta Peak", "Nilgiris", ["ghat", "mountain"]) is True
    assert itin.is_ghat_location("Kapaleeshwarar Temple", "Chennai", ["temple"]) is False

    from models import ItineraryStop
    stop_cbe = ItineraryStop(
        stop_id="s1", type="poi", name="Adiyogi Shiva, Coimbatore", category="Heritage",
        start_time="09:00", end_time="10:30", duration_minutes=90, cost_for_group=0,
        lat=10.9723, lng=76.7408, description="Adiyogi", recommendation_reason="Top rated",
        district="Coimbatore"
    )
    stop_ooty = ItineraryStop(
        stop_id="s2", type="poi", name="Doddabetta Peak, Ooty", category="Nature & Plantations",
        start_time="14:00", end_time="15:30", duration_minutes=90, cost_for_group=60,
        lat=11.4010, lng=76.7356, description="Peak", recommendation_reason="High peak",
        district="Nilgiris"
    )

    seg = itin.estimate_travel_segment(stop_cbe, stop_ooty, "Local Taxi / Cab")
    assert seg.is_ghat_route is True
    assert seg.hairpin_bends == 36
    assert seg.buffer_minutes == 25
    assert "26 km/h" in seg.scenic_note
    # Distance is ~47 km, at 26 km/h = ~108 min + 25m buffer = ~133m
    assert seg.travel_time_minutes >= 120

def test_cross_district_daily_plans_generation():
    """Test generating a full cross-district itinerary from natural language."""
    req = TripGenerateRequest(
        prompt="Plan a 3-day Coimbatore and Ooty trip for 15,000 with Kongu food and tea"
    )
    trip = generate_trip(req)
    assert len(trip.daily_plans) == 3
    
    # Verify Day 1 is in Coimbatore and Day 2/3 explore Nilgiris/Ooty
    day1 = trip.daily_plans[0]
    day2 = trip.daily_plans[1]
    day3 = trip.daily_plans[2]
    
    assert "Coimbatore" in day1.title or "Coimbatore" in day1.stops[0].name or day1.stops[0].district == "Coimbatore"
    assert "Ooty" in day2.title or "Nilgiri" in day2.title or "Mettupalayam" in day2.title
    assert "Ooty" in day3.title or "Peaks" in day3.title or "Blue Mountains" in day3.theme
    
    # Verify mountain transit buffer note appears in feasibility notes
    all_notes = " ".join(day2.feasibility_notes + day3.feasibility_notes)
    assert "Mountain transit buffer applied" in all_notes or "Ghat road speed" in all_notes
