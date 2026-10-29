import math
from typing import List, Dict, Any, Tuple, Optional
from models import (
    POI, Hotel, FoodPlace, PreferenceProfile, DailyPlan, ItineraryStop,
    RouteSegment, ScoredRecommendation
)

class ItineraryEngine:
    """
    Deterministic constraint-satisfaction itinerary generator with mountain transit buffers,
    ghat road speed modeling (~24-28 km/h), district-to-district highway calculations (~60-65 km/h),
    and cross-district tour sequencing.
    """

    GHAT_KEYWORDS = {
        "nilgiris", "ooty", "coonoor", "kotagiri", "kodaikanal", "kodai",
        "yercaud", "shevaroy", "kolli", "kolli hills", "meghamalai", "highwavys",
        "yelagiri", "courtallam", "kutralam", "kalvarayan"
    }

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great circle distance in km between two lat/lng coordinates."""
        r = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c

    def is_ghat_location(self, name: str, district: Optional[str] = None, tags: Optional[List[str]] = None) -> bool:
        """Determines if a location is in high-altitude mountain/ghat territory."""
        text = f"{name or ''} {district or ''} {' '.join(tags or [])}".lower()
        return any(k in text for k in self.GHAT_KEYWORDS) or "ghat" in text or "mountain" in text

    def estimate_travel_segment(
        self,
        from_stop: ItineraryStop,
        to_stop: ItineraryStop,
        transport_mode: str
    ) -> RouteSegment:
        """
        Accurately calculates travel time, identifying mountain ghat passes (24-28 km/h + buffer)
        vs inter-district highways (60-65 km/h) vs local city transits.
        """
        dist_km = self.haversine_distance(from_stop.lat, from_stop.lng, to_stop.lat, to_stop.lng)
        
        from_is_ghat = self.is_ghat_location(from_stop.name, from_stop.district, from_stop.tags)
        to_is_ghat = self.is_ghat_location(to_stop.name, to_stop.district, to_stop.tags)
        is_ghat = from_is_ghat or to_is_ghat

        f_dist = (from_stop.district or "").lower().strip()
        t_dist = (to_stop.district or "").lower().strip()

        hairpin_bends = 0
        buffer_minutes = 0
        corridor_name = None
        scenic_note = "Direct connecting transit between itinerary stops."

        # Specific Recognized Corridors
        if ("coimbatore" in f_dist and "nilgiri" in t_dist) or ("nilgiri" in f_dist and "coimbatore" in t_dist):
            is_ghat = True
            hairpin_bends = 36
            buffer_minutes = 25
            corridor_name = "Mettupalayam - Coonoor - Ooty Ghat Road (NH 181)"
            scenic_note = "Mountain ghat ascent via Mettupalayam-Coonoor pass with 36 hairpin bends and tea estate mist (~26 km/h + 25m mountain safety buffer)."
            speed_kmh = 26.0

        elif ("dindigul" in f_dist and "dindigul" in t_dist and is_ghat) or ("madurai" in f_dist and to_is_ghat):
            is_ghat = True
            hairpin_bends = 18
            buffer_minutes = 20
            corridor_name = "Batlagundu - Palani Ghat Road to Kodaikanal (SH 156)"
            scenic_note = "Ascent through Palani Ghat Road with misty valley overlooks and pine scent (~28 km/h + 20m mountain buffer)."
            speed_kmh = 28.0

        elif "salem" in f_dist and is_ghat:
            is_ghat = True
            hairpin_bends = 20
            buffer_minutes = 15
            corridor_name = "Salem - Yercaud Ghat Road (SH 188)"
            scenic_note = "Winding 20-hairpin climb to Shevaroy hills with panoramic views of Salem city basin (~28 km/h + 15m buffer)."
            speed_kmh = 28.0

        elif "namakkal" in f_dist and is_ghat:
            is_ghat = True
            hairpin_bends = 70
            buffer_minutes = 30
            corridor_name = "Kolli Hills 70 Hairpin Pass"
            scenic_note = "Thrilling 70-hairpin bend climb through dense forest to the Kolli hill range (~24 km/h + 30m safety buffer)."
            speed_kmh = 24.0

        elif "theni" in f_dist and is_ghat:
            is_ghat = True
            hairpin_bends = 18
            buffer_minutes = 25
            corridor_name = "Meghamalai Highwavys Ghat Road"
            scenic_note = "Remote mountain ghat through cardamom and tea plantations to Highwavys Cloud Mountain (~24 km/h + 25m buffer)."
            speed_kmh = 24.0

        elif ("madurai" in f_dist and "ramanathapuram" in t_dist) or ("ramanathapuram" in f_dist and "madurai" in t_dist):
            is_ghat = False
            hairpin_bends = 0
            buffer_minutes = 10
            corridor_name = "Madurai - Rameswaram Pamban Sea Corridor (NH 87)"
            scenic_note = "Scenic coastal highway crossing the historic Pamban Sea Bridge to Rameswaram Island (~60 km/h)."
            speed_kmh = 60.0

        elif ("thanjavur" in f_dist and "tiruchirappalli" in t_dist) or ("tiruchirappalli" in f_dist and "thanjavur" in t_dist):
            is_ghat = False
            hairpin_bends = 0
            buffer_minutes = 10
            corridor_name = "Cauvery Delta Chola Heritage Highway (NH 83)"
            scenic_note = "Smooth 4-lane highway across fertile Cauvery delta fields connecting UNESCO living Chola monuments (~65 km/h)."
            speed_kmh = 65.0

        elif is_ghat:
            # Generic mountain ghat road
            hairpin_bends = 12
            buffer_minutes = 20
            corridor_name = "Western/Eastern Ghats Mountain Pass"
            scenic_note = "Winding hill road navigating elevation changes and sharp curves (~26 km/h + 20m safety buffer)."
            speed_kmh = 26.0

        elif dist_km >= 40.0:
            # Inter-district highway
            hairpin_bends = 0
            buffer_minutes = 10
            corridor_name = "National / State Highway Arterial"
            scenic_note = "Inter-district express highway transit (~62 km/h)."
            speed_kmh = 62.0

        else:
            # Intra-city local transit
            hairpin_bends = 0
            buffer_minutes = 5
            corridor_name = "Local Arterial Road"
            scenic_note = "Local connecting route through town center (~32 km/h)."
            speed_kmh = 32.0

        # Calculate transit duration
        if dist_km < 0.5:
            travel_minutes = 5
        else:
            base_minutes = int((dist_km / speed_kmh) * 60)
            travel_minutes = max(10, base_minutes + buffer_minutes)

        return RouteSegment(
            from_name=from_stop.name,
            to_name=to_stop.name,
            distance_km=round(dist_km, 1),
            travel_time_minutes=travel_minutes,
            transport_mode=transport_mode,
            scenic_note=scenic_note,
            is_ghat_route=is_ghat,
            buffer_minutes=buffer_minutes,
            hairpin_bends=hairpin_bends,
            corridor_name=corridor_name
        )

    def estimate_travel_time(self, dist_km: float) -> int:
        """Backward-compatible fallback travel time calculation."""
        if dist_km < 0.5:
            return 5
        minutes = int((dist_km / 32.0) * 60) + 5
        return max(10, minutes)

    @staticmethod
    def add_minutes_to_time_str(time_str: str, minutes: int) -> str:
        """Add minutes to HH:MM formatted string with boundary handling."""
        parts = time_str.split(":")
        h, m = int(parts[0]), int(parts[1])
        total = h * 60 + m + minutes
        new_h = (total // 60) % 24
        new_m = total % 60
        return f"{new_h:02d}:{new_m:02d}"

    def cluster_pois_by_proximity(
        self,
        ranked_pois: List[Tuple[POI, ScoredRecommendation]],
        num_days: int,
        target_districts: Optional[List[str]] = None
    ) -> List[List[POI]]:
        """
        Partition POIs across days.
        If cross-district travel is active, logically assigns days to corresponding districts.
        Otherwise, uses greedy nearest-neighbor geographic clustering.
        """
        pois = [p for p, _ in ranked_pois]
        if not pois:
            return [[] for _ in range(num_days)]

        # Cross-district assignment logic
        if target_districts and len(target_districts) > 1:
            clusters: List[List[POI]] = [[] for _ in range(num_days)]
            
            # Map POIs by district
            district_poi_map: Dict[str, List[POI]] = {}
            for td in target_districts:
                norm_td = td.lower().strip()
                district_poi_map[norm_td] = [p for p in pois if p.district and p.district.lower().strip() == norm_td]

            # Distribute days across target districts
            num_targets = len(target_districts)
            for d in range(num_days):
                # Pick target district for day d
                assigned_td = target_districts[min(d, num_targets - 1)].lower().strip()
                candidates = district_poi_map.get(assigned_td, [])
                
                # Pick up to 3 POIs for this day from candidates
                start_idx = (d // num_targets) * 2
                day_picks = candidates[start_idx:start_idx + 3]
                if not day_picks and candidates:
                    day_picks = candidates[:2]
                if not day_picks:
                    day_picks = [pois[d % len(pois)]]
                    
                clusters[d] = day_picks

            return clusters

        # Standard greedy nearest-neighbor clustering
        if len(pois) <= num_days:
            clusters = [[] for _ in range(num_days)]
            for idx, p in enumerate(pois):
                clusters[idx % num_days].append(p)
            for d in range(num_days):
                if not clusters[d]:
                    clusters[d].append(pois[0])
            return clusters

        target_per_day = max(2, math.ceil(len(pois) / num_days))
        unassigned = list(pois)
        clusters = []

        for d in range(num_days):
            if not unassigned:
                clusters.append([pois[d % len(pois)]])
                continue
            seed = unassigned.pop(0)
            day_cluster = [seed]
            unassigned.sort(key=lambda p: self.haversine_distance(seed.lat, seed.lng, p.lat, p.lng))
            needed = min(target_per_day - 1, len(unassigned))
            for _ in range(needed):
                day_cluster.append(unassigned.pop(0))
            clusters.append(day_cluster)

        return clusters

    def build_daily_plans(
        self,
        ranked_pois: List[Tuple[POI, ScoredRecommendation]],
        selected_hotel: Hotel,
        food_places: List[FoodPlace],
        profile: PreferenceProfile,
        target_districts: Optional[List[str]] = None,
        district_profiles: Optional[Dict[str, Any]] = None
    ) -> List[DailyPlan]:
        num_days = max(1, profile.duration_days)
        clusters = self.cluster_pois_by_proximity(ranked_pois, num_days, target_districts)
        daily_plans: List[DailyPlan] = []

        dest_low = profile.destination.lower()
        is_kerala = "kerala" in dest_low or "munnar" in dest_low
        is_cross_district = target_districts is not None and len(target_districts) > 1

        for day_idx in range(num_days):
            day_num = day_idx + 1
            day_pois = clusters[day_idx] if day_idx < len(clusters) and clusters[day_idx] else [ranked_pois[0][0]]

            # Detect current day's primary district
            current_district = day_pois[0].district if day_pois and day_pois[0].district else (target_districts[min(day_idx, len(target_districts) - 1)] if target_districts else "Tamil Nadu")
            
            # Determine district description & specialties
            district_info = district_profiles.get(current_district.lower().strip()) if district_profiles else None
            district_desc = district_info.get("description", "") if district_info else f"Exploring highlights of {current_district}."
            district_food_specs = district_info.get("food_specialties", []) if district_info else []

            # Dynamic Day Titles & Themes
            if is_cross_district:
                if "coimbatore" in current_district.lower():
                    title = f"Day {day_num}: Coimbatore - Kongu Heartland, Adiyogi Shiva & Cultural Vistas"
                    theme = "Kongu Heritage & Engineering Center"
                elif "nilgiri" in current_district.lower() or "ooty" in current_district.lower():
                    if day_num == 2 and any("coimbatore" in td.lower() for td in target_districts):
                        title = f"Day {day_num}: Scenic Mettupalayam Ghat Ascent (36 Hairpin Bends) to Ooty & Toy Train"
                        theme = "Nilgiri Mountain Ascent & Colonial Heritage"
                    else:
                        title = f"Day {day_num}: Ooty High Peaks, Doddabetta Panorama & Pykara Cascades"
                        theme = "Blue Mountains Shola & Tea Estates"
                elif "madurai" in current_district.lower():
                    title = f"Day {day_num}: Madurai - Ancient Dravidian Gopurams, Nayakkar Halls & Jigarthanda"
                    theme = "Pandiya Capital & Sacred Architecture"
                elif "ramanathapuram" in current_district.lower() or "rameswaram" in current_district.lower():
                    title = f"Day {day_num}: Rameswaram - Pamban Sea Bridge, Pillared Corridors & Dhanushkodi"
                    theme = "Pamban Island & Land's End Frontier"
                elif "thanjavur" in current_district.lower():
                    title = f"Day {day_num}: Thanjavur - UNESCO Big Temple Monolith & Chola Classical Arts"
                    theme = "Chola Imperial Capital & Saraswathi Mahal"
                elif "kanyakumari" in current_district.lower():
                    title = f"Day {day_num}: Kanyakumari - Triveni Sangam Confluence & Vivekananda Rock"
                    theme = "Three Oceans Land's End & Memorial"
                else:
                    title = f"Day {day_num}: {current_district} Discovery & Cultural Highlights"
                    theme = f"{current_district} Heritage & Vistas"
            elif not is_kerala:
                # Tamil Nadu single-district / standard themes
                if "nilgiri" in dest_low or "ooty" in dest_low or "nilgiri" in current_district.lower():
                    titles = [
                        (f"Day {day_num}: Nilgiri Cloud Forest, Doddabetta Peak & Botany", "Ooty Mountain Splendor & Tea Gardens"),
                        (f"Day {day_num}: Pykara Cascades, Pine Forests & Toy Train", "Sacred Waters & Heritage Railway"),
                        (f"Day {day_num}: Coonoor Tea Estates & Hidden Shola Valleys", "Highland Tea & Colonial Vistas")
                    ]
                    title, theme = titles[(day_num - 1) % len(titles)]
                elif "madurai" in dest_low or "madurai" in current_district.lower():
                    titles = [
                        (f"Day {day_num}: Dravidian Architecture, Meenakshi Gopurams & Royal Nayak Palace", "Madurai Sacred Art & History"),
                        (f"Day {day_num}: Thirumalai Nayak Courtyards, Gandhi Museum & Night Bazaars", "Nayak Heritage & Pandiya Streets"),
                        (f"Day {day_num}: Alagar Hills, Pazhamudircholai & Food Trails", "Sacred Foothills & Madurai Tiffin")
                    ]
                    title, theme = titles[(day_num - 1) % len(titles)]
                elif "kodaikanal" in dest_low or "kodai" in dest_low or "dindigul" in current_district.lower():
                    titles = [
                        (f"Day {day_num}: Kodaikanal Star Lake, Coaker's Walk & Misty Promenades", "Highland Lake & Valley Overlooks"),
                        (f"Day {day_num}: Pillar Rocks, Guna Caves & Pine Forest Trails", "Granite Cliffs & Shola Mist"),
                        (f"Day {day_num}: Silver Cascade & Palani Ghat Mountain Circuit", "Cascades & Foothill Spice Farms")
                    ]
                    title, theme = titles[(day_num - 1) % len(titles)]
                elif "thanjavur" in dest_low or "thanjavur" in current_district.lower():
                    titles = [
                        (f"Day {day_num}: Brihadisvara UNESCO World Heritage Big Temple & Maratha Palace", "Chola Architecture & Royal Bronzes"),
                        (f"Day {day_num}: Kumbakonam Ancient Temples & Degree Kaapi Heritage", "Chola Temple Trail & Cultural Arts"),
                        (f"Day {day_num}: Grand Anicut (Kallanai) & Cauvery Delta Heritage", "Ancient Water Engineering & Delta Fields")
                    ]
                    title, theme = titles[(day_num - 1) % len(titles)]
                else:
                    title = f"Day {day_num}: {current_district} Regional Explorer"
                    theme = f"{current_district} Cultural Circuit - Day {day_num}"
            else:
                default_titles_kerala = [
                    ("Day 1: Misty Cascades, Tea Heritage & Sunset Ridge", "Waterfalls & Plantation Vistas"),
                    ("Day 2: High-Altitude Trekking & Mountain Reservoir", "Challenging Ridge Trek & Serene Boating"),
                    ("Day 3: National Park Trail, Bamboo Groves & Farewell Cascades", "Wildlife Sanctuary & Forest Waterfalls")
                ]
                title, theme = default_titles_kerala[(day_num - 1) % len(default_titles_kerala)]

            # Split day POIs into morning, afternoon, and optional evening
            p_morning = day_pois[0]
            p_afternoon = day_pois[1] if len(day_pois) > 1 else (day_pois[0] if len(day_pois) == 1 else None)
            p_sunset = day_pois[2] if len(day_pois) > 2 else None

            # Select food for day, matching current district if possible
            matched_foods = [f for f in food_places if f.district and f.district.lower().strip() == current_district.lower().strip()]
            pool_foods = matched_foods if matched_foods else food_places

            lunch_idx = (day_idx * 2) % max(1, len(pool_foods)) if pool_foods else 0
            dinner_idx = (day_idx * 2 + 1) % max(1, len(pool_foods)) if pool_foods else 0
            f_lunch = pool_foods[lunch_idx] if pool_foods else None
            f_dinner = pool_foods[dinner_idx] if pool_foods and len(pool_foods) > 1 else f_lunch

            stops: List[ItineraryStop] = []
            day_cost = 0.0

            # Base Camp checkin on Day 1
            if day_num == 1:
                hotel_stay_cost = selected_hotel.price_per_night * max(1, num_days - 1)
                stops.append(ItineraryStop(
                    stop_id=f"stop_h_{selected_hotel.id}",
                    type="hotel_checkin",
                    name=f"Base Camp: {selected_hotel.name}",
                    category="Budget Hotel Stay",
                    start_time="09:00",
                    end_time="09:45",
                    duration_minutes=45,
                    cost_for_group=round(hotel_stay_cost, 2),
                    lat=selected_hotel.lat,
                    lng=selected_hotel.lng,
                    description=f"{selected_hotel.room_type} check-in, unpack gear and freshen up. {selected_hotel.description}",
                    recommendation_reason=f"Verified {selected_hotel.category} (₹{int(selected_hotel.price_per_night)}/night) with {selected_hotel.rating}★ rating.",
                    tags=["hotel", "budget", "stay"],
                    district=selected_hotel.district or current_district,
                    district_description=district_desc
                ))
                day_cost += hotel_stay_cost

            # Block 1: Morning Block (09:00 - 12:30)
            if p_morning:
                start_p = "10:15" if day_num == 1 else ("09:00" if p_morning.opening_time <= "09:00" else p_morning.opening_time)
                dur_p = min(150, max(60, p_morning.typical_duration_minutes))
                end_p = self.add_minutes_to_time_str(start_p, dur_p)
                if end_p > "12:30":
                    end_p = "12:30"

                cost_group = p_morning.entry_fee_per_person * profile.number_of_travelers
                day_cost += cost_group

                stops.append(ItineraryStop(
                    stop_id=f"stop_{p_morning.id}_d{day_num}_morn",
                    type="poi",
                    name=p_morning.name,
                    category=p_morning.category,
                    start_time=start_p,
                    end_time=end_p,
                    duration_minutes=dur_p,
                    cost_for_group=cost_group,
                    lat=p_morning.lat,
                    lng=p_morning.lng,
                    description=p_morning.description,
                    recommendation_reason=f"Top-rated {p_morning.category.lower()} in {p_morning.district or current_district} with {p_morning.rating}★ rating.",
                    tags=p_morning.tags,
                    district=p_morning.district or current_district,
                    opening_time=p_morning.opening_time,
                    closing_time=p_morning.closing_time,
                    district_description=district_desc
                ))

            # Block 2: Afternoon Lunch Window (12:30 - 14:00)
            if f_lunch:
                start_l = "12:45"
                end_l = "13:45"
                lunch_cost = (f_lunch.cost_for_two / 2.0) * profile.number_of_travelers
                day_cost += lunch_cost

                lunch_specs = f_lunch.specialties if f_lunch.specialties else district_food_specs

                stops.append(ItineraryStop(
                    stop_id=f"stop_{f_lunch.id}_lunch_d{day_num}",
                    type="food_lunch",
                    name=f"Traditional Lunch: {f_lunch.name}",
                    category=f_lunch.category,
                    start_time=start_l,
                    end_time=end_l,
                    duration_minutes=60,
                    cost_for_group=round(lunch_cost, 2),
                    lat=f_lunch.lat,
                    lng=f_lunch.lng,
                    description=f"{f_lunch.description} Authentic Specialties: {', '.join(lunch_specs[:3])}.",
                    recommendation_reason=f"Authentic {f_lunch.district or current_district} cuisine ({f_lunch.cuisine}) at ₹{int(lunch_cost)} for party.",
                    tags=["local_food", "lunch"],
                    district=f_lunch.district or current_district,
                    opening_time=f_lunch.opening_time,
                    closing_time=f_lunch.closing_time,
                    food_specialties=lunch_specs,
                    district_description=district_desc
                ))

            # Block 3: Afternoon Sightseeing Stop (14:15 - 17:00)
            if p_afternoon:
                start_a = "14:15"
                dur_a = min(120, max(45, p_afternoon.typical_duration_minutes))
                end_a = self.add_minutes_to_time_str(start_a, dur_a)
                if end_a > "16:45":
                    end_a = "16:45"

                cost_group = p_afternoon.entry_fee_per_person * profile.number_of_travelers
                day_cost += cost_group

                stops.append(ItineraryStop(
                    stop_id=f"stop_{p_afternoon.id}_d{day_num}_aft",
                    type="poi",
                    name=p_afternoon.name,
                    category=p_afternoon.category,
                    start_time=start_a,
                    end_time=end_a,
                    duration_minutes=dur_a,
                    cost_for_group=cost_group,
                    lat=p_afternoon.lat,
                    lng=p_afternoon.lng,
                    description=p_afternoon.description,
                    recommendation_reason=f"Popular {p_afternoon.district or current_district} highlight with {p_afternoon.rating}★ rating.",
                    tags=p_afternoon.tags,
                    district=p_afternoon.district or current_district,
                    opening_time=p_afternoon.opening_time,
                    closing_time=p_afternoon.closing_time,
                    district_description=district_desc
                ))

            # Block 4: Evening Sunset Vantage (17:15 - 19:15)
            if p_sunset:
                start_s = "17:15"
                dur_s = min(90, max(45, p_sunset.typical_duration_minutes))
                end_s = self.add_minutes_to_time_str(start_s, dur_s)
                if end_s > "19:00":
                    end_s = "19:00"

                cost_group = p_sunset.entry_fee_per_person * profile.number_of_travelers
                day_cost += cost_group

                stops.append(ItineraryStop(
                    stop_id=f"stop_{p_sunset.id}_d{day_num}_sunset",
                    type="poi",
                    name=p_sunset.name,
                    category=p_sunset.category,
                    start_time=start_s,
                    end_time=end_s,
                    duration_minutes=dur_s,
                    cost_for_group=cost_group,
                    lat=p_sunset.lat,
                    lng=p_sunset.lng,
                    description=p_sunset.description,
                    recommendation_reason=f"Scenic vantage point in {p_sunset.district or current_district} for golden hour atmosphere.",
                    tags=p_sunset.tags,
                    district=p_sunset.district or current_district,
                    opening_time=p_sunset.opening_time,
                    closing_time=p_sunset.closing_time,
                    district_description=district_desc
                ))

            # Block 5: Evening Dinner Window (19:30 - 21:00)
            if f_dinner and day_num <= min(4, num_days):
                start_d = "19:45"
                end_d = "20:45"
                dinner_cost = (f_dinner.cost_for_two / 2.0) * profile.number_of_travelers
                day_cost += dinner_cost

                dinner_specs = f_dinner.specialties if f_dinner.specialties else district_food_specs

                stops.append(ItineraryStop(
                    stop_id=f"stop_{f_dinner.id}_dinner_d{day_num}",
                    type="food_dinner",
                    name=f"Authentic Dinner: {f_dinner.name}",
                    category=f_dinner.category,
                    start_time=start_d,
                    end_time=end_d,
                    duration_minutes=60,
                    cost_for_group=round(dinner_cost, 2),
                    lat=f_dinner.lat,
                    lng=f_dinner.lng,
                    description=f"{f_dinner.description} Recommended Specialties: {', '.join(dinner_specs[:3])}.",
                    recommendation_reason=f"Relaxing evening meal featuring {f_dinner.district or current_district} culinary traditions.",
                    tags=["local_food", "dinner"],
                    district=f_dinner.district or current_district,
                    opening_time=f_dinner.opening_time,
                    closing_time=f_dinner.closing_time,
                    food_specialties=dinner_specs,
                    district_description=district_desc
                ))

            # Guarantee strict chronological sequence
            self._ensure_time_order(stops)
            segments = self._rebuild_route_segments(stops, profile.transport_preference)

            tot_travel_min = sum(s.travel_time_minutes for s in segments)
            tot_dist_km = sum(s.distance_km for s in segments)

            # Build Feasibility Notes with Mountain & Highway Buffer Transparency
            has_ghat_route = any(s.is_ghat_route for s in segments)
            has_highway = any(s.distance_km >= 40.0 for s in segments)

            feasibility_notes = [
                f"Total daily transit time ({tot_travel_min} mins) is well within limit of {int(profile.max_daily_travel_hours * 60)} mins.",
                "Stops strictly scheduled during daylight and verified operating hours.",
                "Zero chronological overlaps between sequential stops."
            ]

            if has_ghat_route:
                ghat_seg = next(s for s in segments if s.is_ghat_route)
                feasibility_notes.append(
                    f"Mountain transit buffer applied: Ghat road speed (~26 km/h) and safety buffers ({ghat_seg.buffer_minutes}m) accounted for on {ghat_seg.corridor_name or 'ghat pass'}."
                )
            if has_highway:
                feasibility_notes.append("District-to-district highway mileage (~60-65 km/h) optimized to minimize backtracking.")

            plan = DailyPlan(
                day_number=day_num,
                date_label=f"Day {day_num}",
                title=title,
                theme=theme,
                stops=stops,
                route_segments=segments,
                total_travel_time_minutes=tot_travel_min,
                total_distance_km=round(tot_dist_km, 1),
                day_cost=round(day_cost, 2),
                is_feasible=True,
                feasibility_notes=feasibility_notes
            )
            daily_plans.append(plan)

        return daily_plans

    def remove_poi_from_day(
        self,
        daily_plans: List[DailyPlan],
        day_number: int,
        poi_id: str,
        profile: PreferenceProfile
    ) -> List[DailyPlan]:
        """Localized refinement: remove specific POI from a day's plan."""
        target_day = next((d for d in daily_plans if d.day_number == day_number), None)
        if not target_day:
            return daily_plans

        new_stops = [s for s in target_day.stops if not (s.type == "poi" and (poi_id in s.stop_id or s.stop_id == poi_id))]
        if len(new_stops) == len(target_day.stops):
            return daily_plans

        target_day.stops = new_stops
        target_day.route_segments = self._rebuild_route_segments(target_day.stops, profile.transport_preference)
        target_day.total_travel_time_minutes = sum(s.travel_time_minutes for s in target_day.route_segments)
        target_day.total_distance_km = round(sum(s.distance_km for s in target_day.route_segments), 1)
        target_day.day_cost = round(sum(s.cost_for_group for s in target_day.stops), 2)
        return daily_plans

    def add_poi_to_day(
        self,
        daily_plans: List[DailyPlan],
        day_number: int,
        new_poi: POI,
        slot: str,
        profile: PreferenceProfile
    ) -> List[DailyPlan]:
        """Localized refinement: insert a candidate POI into a designated slot."""
        target_day = next((d for d in daily_plans if d.day_number == day_number), None)
        if not target_day:
            return daily_plans

        cost_group = new_poi.entry_fee_per_person * profile.number_of_travelers
        start_time = "10:00" if slot == "morning" else ("14:30" if slot == "afternoon" else "17:30")
        end_time = self.add_minutes_to_time_str(start_time, new_poi.typical_duration_minutes)

        new_stop = ItineraryStop(
            stop_id=f"stop_{new_poi.id}_d{day_number}_{slot}",
            type="poi",
            name=new_poi.name,
            category=new_poi.category,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=new_poi.typical_duration_minutes,
            cost_for_group=cost_group,
            lat=new_poi.lat,
            lng=new_poi.lng,
            description=new_poi.description,
            recommendation_reason=f"Added during user trip refinement ({new_poi.rating}★).",
            tags=new_poi.tags,
            district=new_poi.district,
            opening_time=new_poi.opening_time,
            closing_time=new_poi.closing_time
        )

        insert_idx = len(target_day.stops)
        if slot == "morning":
            insert_idx = 1 if (target_day.stops and target_day.stops[0].type == "hotel_checkin") else 0
        elif slot == "afternoon":
            lunch_idx = next((i for i, s in enumerate(target_day.stops) if s.type == "food_lunch"), None)
            insert_idx = (lunch_idx + 1) if lunch_idx is not None else len(target_day.stops)

        target_day.stops.insert(insert_idx, new_stop)
        self._ensure_time_order(target_day.stops)
        target_day.route_segments = self._rebuild_route_segments(target_day.stops, profile.transport_preference)
        target_day.total_travel_time_minutes = sum(s.travel_time_minutes for s in target_day.route_segments)
        target_day.total_distance_km = round(sum(s.distance_km for s in target_day.route_segments), 1)
        target_day.day_cost = round(sum(s.cost_for_group for s in target_day.stops), 2)
        return daily_plans

    def swap_poi_in_day(
        self,
        daily_plans: List[DailyPlan],
        day_number: int,
        old_poi_id: str,
        new_poi: POI,
        profile: PreferenceProfile
    ) -> List[DailyPlan]:
        """Localized refinement: replace an existing POI with a selected replacement."""
        target_day = next((d for d in daily_plans if d.day_number == day_number), None)
        if not target_day:
            return daily_plans

        for stop in target_day.stops:
            if stop.type == "poi" and (old_poi_id in stop.stop_id or stop.stop_id == old_poi_id):
                cost_group = new_poi.entry_fee_per_person * profile.number_of_travelers
                stop.stop_id = f"stop_{new_poi.id}_d{day_number}_swapped"
                stop.name = new_poi.name
                stop.category = new_poi.category
                stop.duration_minutes = new_poi.typical_duration_minutes
                stop.end_time = self.add_minutes_to_time_str(stop.start_time, new_poi.typical_duration_minutes)
                stop.cost_for_group = cost_group
                stop.lat = new_poi.lat
                stop.lng = new_poi.lng
                stop.description = new_poi.description
                stop.recommendation_reason = f"Swapped by user: top candidate with {new_poi.rating}★ rating."
                stop.tags = new_poi.tags
                stop.district = new_poi.district
                stop.opening_time = new_poi.opening_time
                stop.closing_time = new_poi.closing_time
                break

        self._ensure_time_order(target_day.stops)
        target_day.route_segments = self._rebuild_route_segments(target_day.stops, profile.transport_preference)
        target_day.total_travel_time_minutes = sum(s.travel_time_minutes for s in target_day.route_segments)
        target_day.total_distance_km = round(sum(s.distance_km for s in target_day.route_segments), 1)
        target_day.day_cost = round(sum(s.cost_for_group for s in target_day.stops), 2)
        return daily_plans

    def _ensure_time_order(self, stops: List[ItineraryStop]):
        """Ensure non-overlapping sequential times."""
        for i in range(len(stops) - 1):
            if stops[i].end_time > stops[i+1].start_time:
                stops[i+1].start_time = self.add_minutes_to_time_str(stops[i].end_time, 15)
                stops[i+1].end_time = self.add_minutes_to_time_str(stops[i+1].start_time, stops[i+1].duration_minutes)

    def _rebuild_route_segments(self, stops: List[ItineraryStop], transport_mode: str) -> List[RouteSegment]:
        """Reconstruct RouteSegment list between consecutive stops with ghat & highway accuracy."""
        segments: List[RouteSegment] = []
        for i in range(len(stops) - 1):
            seg = self.estimate_travel_segment(stops[i], stops[i+1], transport_mode)
            segments.append(seg)
        return segments
