import pytest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    PreferenceProfile, POI, Hotel, FoodPlace,
    Trip, ScoredRecommendation, RecommendationScoreBreakdown,
    TripGenerateRequest, TripRefineRequest
)
from recommendation_engine import RecommendationEngine
from itinerary_engine import ItineraryEngine
from budget_engine import BudgetEngine
from main import parse_natural_language_prompt, generate_trip, refine_trip, list_pois, get_budget_breakdown

def test_recommendation_scoring_weights():
    engine = RecommendationEngine()
    total_weights = sum(engine.weights.values())
    assert round(total_weights, 4) == 1.0, "Weights must sum to 1.0"

def test_poi_scoring_affinity():
    engine = RecommendationEngine()
    profile = PreferenceProfile(
        destination="Kerala",
        duration_days=3,
        number_of_travelers=2,
        budget=15000.0,
        interests=["Waterfalls", "Trekking"],
        travel_pace="Moderate pace"
    )
    
    waterfall_poi = POI(
        id="poi_test_falls",
        name="Attukad Falls",
        category="Waterfalls",
        tags=["waterfall", "nature"],
        lat=10.05,
        lng=77.04,
        rating=4.6,
        review_count=5000,
        entry_fee_per_person=30,
        typical_duration_minutes=90,
        opening_time="08:00",
        closing_time="18:00",
        description="Scenic falls"
    )

    unrelated_poi = POI(
        id="poi_test_shopping",
        name="Shopping Plaza",
        category="Shopping",
        tags=["mall", "retail"],
        lat=10.05,
        lng=77.04,
        rating=4.0,
        review_count=500,
        entry_fee_per_person=0,
        typical_duration_minutes=60,
        opening_time="10:00",
        closing_time="21:00",
        description="Shopping mall"
    )

    score_falls, breakdown_falls, exp_falls = engine.score_poi(waterfall_poi, profile, 10.05, 77.04)
    score_shop, breakdown_shop, exp_shop = engine.score_poi(unrelated_poi, profile, 10.05, 77.04)

    assert score_falls > score_shop, "Waterfall POI must score higher than unrelated shopping POI for waterfall interest"
    assert breakdown_falls.preference_match > breakdown_shop.preference_match
    assert 0.0 <= score_falls <= 1.0

def test_budget_engine_calculation():
    budget_engine = BudgetEngine()
    profile = PreferenceProfile(
        destination="Kerala",
        duration_days=3,
        number_of_travelers=2,
        budget=15000.0,
        interests=["Waterfalls", "Trekking"],
        hotel_preference="Budget Hotel"
    )
    hotel = Hotel(
        id="hotel_test",
        name="Test Homestay",
        category="Budget Hotel",
        price_per_night=1500.0,
        rating=4.5,
        review_count=300,
        lat=10.08,
        lng=77.06,
        address="Munnar",
        amenities=["WiFi"],
        room_type="Standard Double",
        description="Nice stay"
    )

    summary = budget_engine.compute_budget_summary(profile, hotel, [])
    assert summary.within_budget is True, "₹15,000 budget for 2 travelers over 3 days should be within budget with a ₹1,500/night hotel"
    assert summary.total_expected_cost < 15000.0
    assert summary.budget_remaining > 0
    assert len(summary.items) == 5

def test_itinerary_feasibility_no_overlap():
    itin_engine = ItineraryEngine()
    profile = PreferenceProfile(
        destination="Kerala",
        duration_days=3,
        number_of_travelers=2,
        budget=15000.0,
        interests=["Waterfalls", "Trekking"]
    )
    hotel = Hotel(
        id="hotel_test",
        name="Test Homestay",
        category="Budget Hotel",
        price_per_night=1500.0,
        rating=4.5,
        review_count=300,
        lat=10.08,
        lng=77.06,
        address="Munnar",
        amenities=["WiFi"],
        room_type="Standard Double",
        description="Nice stay"
    )
    p1 = POI(
        id="p1", name="Falls 1", category="Waterfalls", tags=["waterfall"],
        lat=10.05, lng=77.04, rating=4.5, review_count=100, entry_fee_per_person=50,
        typical_duration_minutes=90, opening_time="08:00", closing_time="18:00", description="Falls"
    )
    rec = ScoredRecommendation(
        item_id="p1", name="Falls 1", category="Waterfalls",
        scores=RecommendationScoreBreakdown(preference_match=1, context_match=1, distance_score=1, quality_score=1, budget_fit=1, schedule_fit=1, total_score=1),
        primary_explanation="Great", tags=[]
    )
    food = FoodPlace(
        id="f1", name="Food 1", category="Local Food", cuisine="Kerala",
        specialties=["Parotta"], cost_for_two=300, rating=4.5, review_count=200,
        lat=10.08, lng=77.06, opening_time="07:00", closing_time="22:00", description="Food"
    )

    plans = itin_engine.build_daily_plans([(p1, rec)], hotel, [food], profile)
    assert len(plans) == 3, "Must generate 3 daily plans"
    for plan in plans:
        assert plan.is_feasible is True
        # Check chronological order of stops
        for i in range(len(plan.stops) - 1):
            assert plan.stops[i].end_time <= plan.stops[i+1].start_time, f"Stop {plan.stops[i].name} overlaps with {plan.stops[i+1].name}"

def test_nlp_parser_extraction():
    prompt = "Plan a 3-day Kerala trip for 15,000 with waterfalls and local food"
    res = parse_natural_language_prompt(prompt)
    assert res.destination == "Kerala"
    assert res.duration_days == 3
    assert res.budget == 15000.0
    assert "Waterfalls" in res.interests
    assert res.food_preference == "Local Food"
    assert res.budget_tier == "Budget"
    assert res.confidence >= 0.85

def test_nlp_parser_goa_and_k_notation():
    prompt = "4-day Goa beach vacation for 25k with seafood"
    res = parse_natural_language_prompt(prompt)
    assert res.destination == "Goa"
    assert res.duration_days == 4
    assert res.budget == 25000.0
    assert "Beaches" in res.interests
    assert res.food_preference == "Seafood Specialties"
    assert res.budget_tier == "Moderate"

def test_trip_generation_and_refine_pipeline():
    # 1. Generate full trip from prompt
    req = TripGenerateRequest(prompt="Plan a 3-day Kerala trip for 15,000 with waterfalls and local food")
    trip = generate_trip(req)
    assert trip.status == "planned"
    assert len(trip.daily_plans) == 3
    assert trip.budget_summary is not None
    assert trip.selected_hotel is not None
    initial_hotel_id = trip.selected_hotel.id

    # 2. Refine trip by swapping hotel
    # Find another hotel from Kerala
    from main import get_destination_data
    kerala_data = get_destination_data("Kerala")
    hotels = kerala_data["hotels"]
    alt_hotel = next(h for h in hotels if h["id"] != initial_hotel_id)

    refine_req = TripRefineRequest(
        trip_id=trip.trip_id,
        action="swap_hotel",
        hotel_id=alt_hotel["id"]
    )
    refine_res = refine_trip(refine_req)
    assert refine_res.success is True
    assert refine_res.trip.selected_hotel.id == alt_hotel["id"]

    # 3. Refine trip by removing a POI stop from Day 1
    day1_pois = [s for s in refine_res.trip.daily_plans[0].stops if s.type == "poi"]
    if day1_pois:
        target_poi_id = day1_pois[0].stop_id
        rem_res = refine_trip(TripRefineRequest(
            trip_id=trip.trip_id,
            action="remove_poi",
            day_number=1,
            poi_id=target_poi_id
        ))
        assert rem_res.success is True
        remaining_ids = [s.stop_id for s in rem_res.trip.daily_plans[0].stops]
        assert target_poi_id not in remaining_ids

def test_poi_listing_and_filtering():
    pois = list_pois(destination="Kerala", category="Waterfalls")
    assert len(pois) > 0
    for p in pois:
        assert "waterfall" in p.category.lower()

    # Search filter
    searched = list_pois(destination="Kerala", search="Tea")
    assert len(searched) > 0


def test_nlp_parser_tamilnadu_and_cities():
    # Test Ooty and Madurai prompt
    prompt1 = "Plan a 4-day Ooty and Madurai heritage trip for 12,000 with Chettinad food"
    res1 = parse_natural_language_prompt(prompt1)
    assert res1.destination == "Tamil Nadu"
    assert res1.duration_days == 4
    assert res1.budget == 12000.0
    assert "Heritage" in res1.interests
    assert res1.food_preference == "Chettinad Spicy Traditional"
    assert res1.budget_tier == "Budget"

    # Test Kodaikanal prompt
    prompt2 = "3 days in Kodaikanal for 15k with waterfalls and vegetarian food"
    res2 = parse_natural_language_prompt(prompt2)
    assert res2.destination == "Tamil Nadu"
    assert res2.duration_days == 3
    assert res2.budget == 15000.0
    assert res2.food_preference == "Pure Vegetarian"
    assert "Waterfalls" in res2.interests


def test_tamilnadu_trip_generation():
    req = TripGenerateRequest(prompt="Plan a 4-day Ooty and Madurai heritage trip for 12,000 with Chettinad food")
    trip = generate_trip(req)
    assert trip.status == "planned"
    assert trip.profile.destination == "Tamil Nadu"
    assert len(trip.daily_plans) == 4
    assert trip.selected_hotel is not None
    assert trip.budget_summary is not None

    # Check that Tamil Nadu POIs are selected
    all_stop_names = [s.name for day in trip.daily_plans for s in day.stops]
    assert any("Meenakshi" in n or "Doddabetta" in n or "Pykara" in n or "Botanical" in n or "Temple" in n for n in all_stop_names)

    # Check no time overlap
    for day in trip.daily_plans:
        assert day.is_feasible is True
        for i in range(len(day.stops) - 1):
            assert day.stops[i].end_time <= day.stops[i+1].start_time

    # Check emergency contacts in offline package
    assert trip.offline_package is not None
    assert any("Tamil Nadu" in c["name"] or "Madurai" in c["name"] or "Nilgiris" in c["name"] for c in trip.offline_package.emergency_contacts)


def test_multi_destination_support():
    from main import SEED_DATA
    assert "kerala" in SEED_DATA
    assert "goa" in SEED_DATA
    assert "tamilnadu" in SEED_DATA

    # Check POIs listing across all three states
    pois_kerala = list_pois(destination="Kerala")
    pois_goa = list_pois(destination="Goa")
    pois_tn = list_pois(destination="Tamil Nadu")

    assert len(pois_kerala) >= 5
    assert len(pois_goa) >= 4
    assert len(pois_tn) >= 10

