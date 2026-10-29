export interface PreferenceProfile {
  destination: string;
  duration_days: number;
  number_of_travelers: number;
  budget: number;
  currency: string;
  interests: string[];
  disliked_categories: string[];
  travel_pace: string;
  food_preference: string;
  hotel_preference: string;
  transport_preference: string;
  max_daily_travel_hours: number;
  accessibility_requirements?: string;
  free_text_request?: string;
}

export interface User {
  user_id: string;
  name: string;
  email: string;
  is_demo: boolean;
  profile?: PreferenceProfile;
}

export interface POI {
  id: string;
  name: string;
  category: string;
  tags: string[];
  lat: number;
  lng: number;
  rating: number;
  review_count: number;
  entry_fee_per_person: number;
  typical_duration_minutes: number;
  opening_time: string;
  closing_time: string;
  description: string;
  best_time_to_visit?: string;
  difficulty?: string;
  district?: string;
  elevation_m?: number;
  is_mountain_route?: boolean;
}

export interface Hotel {
  id: string;
  name: string;
  category: string;
  price_per_night: number;
  rating: number;
  review_count: number;
  lat: number;
  lng: number;
  address: string;
  amenities: string[];
  room_type: string;
  description: string;
  district?: string;
}

export interface FoodPlace {
  id: string;
  name: string;
  category: string;
  cuisine: string;
  specialties: string[];
  cost_for_two: number;
  rating: number;
  review_count: number;
  lat: number;
  lng: number;
  opening_time: string;
  closing_time: string;
  description: string;
  district?: string;
}

export interface RouteSegment {
  from_name: string;
  to_name: string;
  distance_km: number;
  travel_time_minutes: number;
  transport_mode: string;
  scenic_note?: string;
  is_ghat_route?: boolean;
  buffer_minutes?: number;
  hairpin_bends?: number;
  corridor_name?: string;
}

export interface ItineraryStop {
  stop_id: string;
  type: string;
  name: string;
  category: string;
  start_time: string;
  end_time: string;
  duration_minutes: number;
  cost_for_group: number;
  lat: number;
  lng: number;
  description: string;
  recommendation_reason: string;
  tags: string[];
  district?: string;
  opening_time?: string;
  closing_time?: string;
  food_specialties?: string[];
  district_description?: string;
}

export interface DailyPlan {
  day_number: number;
  date_label: string;
  title: string;
  theme: string;
  stops: ItineraryStop[];
  route_segments: RouteSegment[];
  total_travel_time_minutes: number;
  total_distance_km: number;
  day_cost: number;
  is_feasible: boolean;
  feasibility_notes: string[];
}

export interface BudgetItem {
  category: string;
  label: string;
  min_cost: number;
  expected_cost: number;
  max_cost: number;
  details: string;
  is_live_price: boolean;
  price_source: string;
}

export interface BudgetSummary {
  total_budget: number;
  total_expected_cost: number;
  min_cost: number;
  max_cost: number;
  currency: string;
  within_budget: boolean;
  budget_remaining: number;
  budget_variance_percentage: number;
  items: BudgetItem[];
  warnings: string[];
}

export interface RecommendationScoreBreakdown {
  preference_match: number;
  context_match: number;
  distance_score: number;
  quality_score: number;
  budget_fit: number;
  schedule_fit: number;
  total_score: number;
}

export interface ScoredRecommendation {
  item_id: string;
  name: string;
  category: string;
  scores: RecommendationScoreBreakdown;
  primary_explanation: string;
  tags: string[];
}

export interface OfflinePackage {
  trip_id: string;
  destination: string;
  generated_at: string;
  expires_at: string;
  travelers_count: number;
  total_budget: number;
  daily_plans: DailyPlan[];
  hotel_details: Hotel;
  food_recommendations: FoodPlace[];
  budget_summary: BudgetSummary;
  emergency_contacts: { name: string; phone: string; type: string }[];
  offline_instructions: string;
  is_offline_ready: boolean;
}

export interface Trip {
  trip_id: string;
  user_id: string;
  status: string;
  profile: PreferenceProfile;
  recommendations: ScoredRecommendation[];
  daily_plans: DailyPlan[];
  selected_hotel?: Hotel;
  selected_food_places: FoodPlace[];
  budget_summary?: BudgetSummary;
  offline_package?: OfflinePackage;
  created_at: string;
  updated_at: string;
}

export interface TripParseResponse {
  destination: string;
  duration_days: number;
  budget: number;
  budget_tier: string;
  number_of_travelers: number;
  interests: string[];
  food_preference: string;
  hotel_preference: string;
  travel_pace: string;
  transport_preference: string;
  confidence: number;
  extracted_entities: Record<string, any>;
  extracted_districts?: string[];
  is_cross_district?: boolean;
}

export interface TripRefineResponse {
  success: boolean;
  action: string;
  message: string;
  trip: Trip;
}

