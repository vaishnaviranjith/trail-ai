import math
from typing import List, Dict, Any, Tuple, Optional
from models import POI, Hotel, FoodPlace, PreferenceProfile, ScoredRecommendation, RecommendationScoreBreakdown

class RecommendationEngine:
    """
    IEEE-inspired normalized multi-feature recommendation engine with granular district awareness.
    Implements multi-objective scoring:
    score = w_pref * preference_match + w_context * context_match + w_dist * distance_score
            + w_rating * quality_score + w_budget * budget_fit + w_time * schedule_fit
    All sub-scores are normalized to [0, 1].
    """
    def __init__(self):
        # Weights normalized to sum to 1.0
        self.weights = {
            "w_pref": 0.30,
            "w_context": 0.15,
            "w_distance": 0.15,
            "w_rating": 0.15,
            "w_budget": 0.15,
            "w_time": 0.10
        }

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great circle distance between two points in km."""
        r = 6371.0 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c

    def score_poi(
        self,
        poi: POI,
        profile: PreferenceProfile,
        anchor_lat: float,
        anchor_lng: float,
        target_districts: Optional[List[str]] = None,
        district_anchors: Optional[Dict[str, Dict[str, float]]] = None
    ) -> Tuple[float, Optional[RecommendationScoreBreakdown], str]:
        # 1. Hard filters
        if poi.category in profile.disliked_categories:
            return 0.0, None, "Excluded by user disliked category"

        # 2. Preference match (category + tags match with user interests + district affinity)
        user_interests = [i.lower() for i in profile.interests]
        poi_terms = [poi.category.lower()] + [t.lower() for t in poi.tags]
        
        match_count = sum(1 for interest in user_interests if any(interest in term or term in interest for term in poi_terms))
        if user_interests:
            preference_match = min(1.0, match_count / max(1, len(user_interests)) + (0.3 if poi.category.lower() in user_interests else 0.0))
            preference_match = min(1.0, preference_match)
        else:
            preference_match = 0.5

        # District affinity boost if POI belongs to requested district(s)
        is_target_district = False
        if target_districts and poi.district:
            norm_targets = [td.lower().strip() for td in target_districts]
            if poi.district.lower().strip() in norm_targets:
                is_target_district = True
                preference_match = min(1.0, preference_match + 0.3)

        # 3. Context match (group size, pace, duration)
        # Moderate pace favors POIs with duration <= 180 min
        context_match = 1.0
        if profile.travel_pace == "Relaxed pace" and poi.typical_duration_minutes > 150:
            context_match -= 0.2
        elif profile.travel_pace == "Fast pace" and poi.typical_duration_minutes < 90:
            context_match += 0.1
        if is_target_district:
            context_match = min(1.0, context_match + 0.15)
        context_match = max(0.2, min(1.0, context_match))

        # 4. Distance score (proximity to anchor coordinates or target district hub)
        effective_anchor_lat = anchor_lat
        effective_anchor_lng = anchor_lng
        
        # If district anchors are provided and POI has a district anchor, measure to that district hub
        if district_anchors and poi.district and poi.district in district_anchors:
            effective_anchor_lat = district_anchors[poi.district]["lat"]
            effective_anchor_lng = district_anchors[poi.district]["lng"]
        elif target_districts and district_anchors:
            # Measure to the closest target district anchor
            min_dist = float('inf')
            for td in target_districts:
                if td in district_anchors:
                    d = self.haversine_distance(district_anchors[td]["lat"], district_anchors[td]["lng"], poi.lat, poi.lng)
                    if d < min_dist:
                        min_dist = d
                        effective_anchor_lat = district_anchors[td]["lat"]
                        effective_anchor_lng = district_anchors[td]["lng"]

        dist_km = self.haversine_distance(effective_anchor_lat, effective_anchor_lng, poi.lat, poi.lng)
        # 0 km -> 1.0, 30 km -> 0.6, 60+ km -> 0.2
        if is_target_district:
            distance_score = max(0.4, 1.0 - (dist_km / 75.0))
        else:
            distance_score = max(0.1, 1.0 - (dist_km / 50.0))

        # 5. Quality score (Rating normalized from [3.5, 5.0] to [0, 1] + log review volume)
        rating_normalized = max(0.0, min(1.0, (poi.rating - 3.5) / 1.5))
        review_bonus = min(0.2, math.log10(max(10, poi.review_count)) / 10.0)
        quality_score = min(1.0, rating_normalized * 0.8 + review_bonus)

        # 6. Budget fit (entry fee for party size vs per-day activity budget)
        total_entry = poi.entry_fee_per_person * profile.number_of_travelers
        daily_budget = profile.budget / max(1, profile.duration_days)
        activity_budget_allocated = daily_budget * 0.25 # 25% for activities
        if total_entry <= activity_budget_allocated:
            budget_fit = 1.0
        else:
            budget_fit = max(0.1, 1.0 - (total_entry - activity_budget_allocated) / activity_budget_allocated)

        # 7. Schedule fit (typical duration fits within day limit)
        max_duration_allowed = 240 if profile.travel_pace == "Fast pace" else 180
        schedule_fit = max(0.2, 1.0 - max(0, poi.typical_duration_minutes - 90) / max_duration_allowed)

        # Weighted composite score
        total_score = (
            self.weights["w_pref"] * preference_match +
            self.weights["w_context"] * context_match +
            self.weights["w_distance"] * distance_score +
            self.weights["w_rating"] * quality_score +
            self.weights["w_budget"] * budget_fit +
            self.weights["w_time"] * schedule_fit
        )

        breakdown = RecommendationScoreBreakdown(
            preference_match=round(preference_match, 3),
            context_match=round(context_match, 3),
            distance_score=round(distance_score, 3),
            quality_score=round(quality_score, 3),
            budget_fit=round(budget_fit, 3),
            schedule_fit=round(schedule_fit, 3),
            total_score=round(total_score, 3)
        )

        # Explainable primary explanation
        reasons = []
        if is_target_district:
            reasons.append(f"Premier highlight of {poi.district}")
        if preference_match >= 0.7:
            reasons.append(f"Direct match for '{poi.category}' interest")
        if quality_score >= 0.8:
            reasons.append(f"Outstanding {poi.rating}★ rating ({poi.review_count:,} reviews)")
        if distance_score >= 0.7:
            reasons.append("Close proximity to itinerary circuit hub")
        if budget_fit >= 0.9:
            reasons.append(f"Highly affordable entry (₹{int(poi.entry_fee_per_person)}/person)")
        explanation = " • ".join(reasons) if reasons else f"Recommended for balanced {profile.travel_pace} itinerary"

        return total_score, breakdown, explanation

    def rank_pois(
        self,
        pois: List[POI],
        profile: PreferenceProfile,
        anchor_lat: float,
        anchor_lng: float,
        target_districts: Optional[List[str]] = None,
        district_anchors: Optional[Dict[str, Dict[str, float]]] = None
    ) -> List[Tuple[POI, ScoredRecommendation]]:
        scored_list = []
        for poi in pois:
            score, breakdown, explanation = self.score_poi(
                poi, profile, anchor_lat, anchor_lng, target_districts, district_anchors
            )
            if score > 0 and breakdown is not None:
                rec = ScoredRecommendation(
                    item_id=poi.id,
                    name=poi.name,
                    category=poi.category,
                    scores=breakdown,
                    primary_explanation=explanation,
                    tags=poi.tags
                )
                scored_list.append((poi, rec))
        
        # Sort descending by total score
        scored_list.sort(key=lambda x: x[1].scores.total_score, reverse=True)
        return scored_list

    def select_best_hotel(
        self,
        hotels: List[Hotel],
        profile: PreferenceProfile,
        anchor_lat: float,
        anchor_lng: float,
        target_districts: Optional[List[str]] = None
    ) -> Hotel:
        """Select best matching hotel based on category, district, and budget constraints."""
        if not hotels:
            return Hotel(
                id="hotel_default",
                name="Central Heritage Residency",
                category="Budget Hotel",
                price_per_night=1800,
                rating=4.4,
                review_count=1000,
                lat=anchor_lat,
                lng=anchor_lng,
                address="Central Hub Road",
                amenities=["Air Conditioning", "Free Wi-Fi"],
                room_type="Deluxe Double Room",
                description="Comfortable central basecamp hotel."
            )

        budget_per_night_target = (profile.budget * 0.35) / max(1, profile.duration_days - 1)
        best_hotel = None
        best_score = -1.0

        primary_district = target_districts[0].lower().strip() if target_districts else None

        for h in hotels:
            cat_match = 1.0 if profile.hotel_preference.lower() in h.category.lower() else 0.6
            price_fit = 1.0 if h.price_per_night <= budget_per_night_target * 1.2 else max(0.2, budget_per_night_target / h.price_per_night)
            dist_km = self.haversine_distance(anchor_lat, anchor_lng, h.lat, h.lng)
            dist_score = max(0.2, 1.0 - (dist_km / 40.0))

            district_boost = 0.0
            if primary_district and h.district and h.district.lower().strip() == primary_district:
                district_boost = 0.25

            score = 0.35 * price_fit + 0.25 * cat_match + 0.2 * (h.rating / 5.0) + 0.1 * dist_score + 0.1 * district_boost

            if score > best_score:
                best_score = score
                best_hotel = h

        return best_hotel or hotels[0]

    def select_food_places(
        self,
        food_places: List[FoodPlace],
        profile: PreferenceProfile,
        count: int = 4,
        target_districts: Optional[List[str]] = None
    ) -> List[FoodPlace]:
        """Select top authentic eateries matching food preferences and district flavors."""
        if not food_places:
            return []

        norm_targets = [td.lower().strip() for td in target_districts] if target_districts else []

        def food_score(fp: FoodPlace):
            pref_match = 1.0 if profile.food_preference.lower() in fp.category.lower() or "tamil" in fp.cuisine.lower() or "chettinad" in fp.cuisine.lower() or "kerala" in fp.cuisine.lower() else 0.5
            price_fit = 1.0 if fp.cost_for_two <= 600 else 0.7
            
            district_bonus = 0.0
            if fp.district and norm_targets:
                if fp.district.lower().strip() in norm_targets:
                    district_bonus = 0.3

            return 0.4 * pref_match + 0.3 * (fp.rating / 5.0) + 0.15 * price_fit + 0.15 * district_bonus

        sorted_food = sorted(food_places, key=food_score, reverse=True)

        if target_districts and len(target_districts) > 1:
            chosen: List[FoodPlace] = []
            for td in target_districts:
                td_food = [f for f in sorted_food if f.district and f.district.lower().strip() == td.lower().strip()]
                if td_food and td_food[0] not in chosen:
                    chosen.append(td_food[0])
            for f in sorted_food:
                if f not in chosen and len(chosen) < count:
                    chosen.append(f)
            return chosen[:count]

        return sorted_food[:count]
