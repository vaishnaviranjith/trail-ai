import React, { useState } from 'react';
import { 
  Sparkles, SlidersHorizontal, ChevronDown, ChevronUp, MapPin, 
  Calendar, IndianRupee, Users, Compass, Check, Mountain, Landmark, Utensils, Waves
} from 'lucide-react';
import { PreferenceProfile } from '../types';

interface NaturalLanguageSearchProps {
  onGenerate: (prompt: string, structuredData?: PreferenceProfile) => void;
  isLoading: boolean;
  defaultPrompt?: string;
  onParsePrompt?: (prompt: string) => Promise<any>;
}

export const NaturalLanguageSearch: React.FC<NaturalLanguageSearchProps> = ({
  onGenerate,
  isLoading,
  defaultPrompt = "Plan a 3-day Coimbatore and Ooty trip for 15,000 with Kongu food and tea",
  onParsePrompt
}) => {
  const [prompt, setPrompt] = useState(defaultPrompt);
  const [showStructured, setShowStructured] = useState(false);
  const [isParsing, setIsParsing] = useState(false);
  const [selectedHub, setSelectedHub] = useState<string>("Kongu Nadu & Coimbatore Hub");

  // Structured fallback form values
  const [destination, setDestination] = useState<string>("Tamil Nadu");
  const [durationDays, setDurationDays] = useState<number>(3);
  const [travelers, setTravelers] = useState<number>(2);
  const [budget, setBudget] = useState<number>(15000);
  const [budgetTier, setBudgetTier] = useState<string>("Budget");
  const [interests, setInterests] = useState<string[]>(["Heritage", "Nature & Plantations"]);
  const [foodPreference, setFoodPreference] = useState<string>("Kongu Nadu Traditional");
  const [hotelPreference, setHotelPreference] = useState<string>("Budget Hotel");
  const [travelPace, setTravelPace] = useState<string>("Moderate pace");
  const [transportPreference, setTransportPreference] = useState<string>("Local Taxi / Cab");

  const availableInterests = [
    "Waterfalls", "Trekking", "Beaches", "Heritage", "Wildlife",
    "Nature & Plantations", "Food & Dining", "Adventure"
  ];

  // 6 Major Tamil Nadu Tourism Hubs as requested
  const tnTourismHubs = [
    {
      id: "kongu",
      title: "Kongu Nadu & Coimbatore Hub",
      badge: "Kovai • Siruvani • Adiyogi",
      icon: Landmark,
      promptText: "Plan a 3-day Coimbatore and Kongu Nadu trip for 14,000 with Annapoorna food and Adiyogi Shiva",
      dest: "Tamil Nadu (Coimbatore)",
      food: "Kongu Nadu Traditional",
      interests: ["Heritage", "Nature & Plantations"]
    },
    {
      id: "nilgiris",
      title: "Nilgiris & Ooty Hills",
      badge: "Doddabetta • Toy Train • Varkey",
      icon: Mountain,
      promptText: "Plan a 3-day Nilgiris and Ooty hill station vacation for 16,000 with tea gardens and Pykara falls",
      dest: "Tamil Nadu (Nilgiris)",
      food: "Nilgiri Highland Tea & Bakes",
      interests: ["Nature & Plantations", "Waterfalls", "Trekking"]
    },
    {
      id: "madurai",
      title: "Madurai & Temple Circuit",
      badge: "Meenakshi • Nayakkar • Jigarthanda",
      icon: Landmark,
      promptText: "Plan a 3-day Madurai heritage and temple circuit for 12,000 with Jigarthanda and Murugan idli",
      dest: "Tamil Nadu (Madurai)",
      food: "Madurai Traditional & Tiffin",
      interests: ["Heritage", "Food & Dining"]
    },
    {
      id: "thanjavur",
      title: "Thanjavur & Chola Heritage",
      badge: "Big Temple • Kumbakonam Kaapi",
      icon: Landmark,
      promptText: "Plan a 3-day Thanjavur and Trichy Chola heritage tour for 13,000 with UNESCO Big Temple and Degree coffee",
      dest: "Tamil Nadu (Thanjavur)",
      food: "Traditional Chola Nadu Tiffin",
      interests: ["Heritage", "Food & Dining"]
    },
    {
      id: "kanyakumari",
      title: "Kanyakumari & Southern Coast",
      badge: "Triveni Sangam • Pamban • Sunrise",
      icon: Waves,
      promptText: "Plan a 4-day Kanyakumari and Rameswaram coastal expedition for 18,000 with Pamban bridge and seafood",
      dest: "Tamil Nadu (Kanyakumari, Ramanathapuram)",
      food: "Seafood Specialties",
      interests: ["Beaches", "Heritage"]
    },
    {
      id: "kodaikanal",
      title: "Kodaikanal Misty Valleys",
      badge: "Pillar Rocks • Pine Forest",
      icon: Mountain,
      promptText: "Plan a 3-day Kodaikanal misty valley retreat for 15,000 with waterfalls, Pillar rocks and Kodai chocolates",
      dest: "Tamil Nadu (Dindigul)",
      food: "Traditional Tamil Non-Veg & Seeraga Samba",
      interests: ["Nature & Plantations", "Waterfalls"]
    }
  ];

  const samplePrompts = [
    {
      title: "Cross-District: Coimbatore to Ooty",
      text: "Plan a 3-day Coimbatore and Ooty trip for 15,000 with Kongu food and tea",
      badge: "Ghat Road NH181"
    },
    {
      title: "Pandiya to Coast: Madurai & Rameswaram",
      text: "Plan a 4-day Madurai to Rameswaram pilgrimage for 16,000 with Pamban bridge",
      badge: "Temple & Ocean"
    },
    {
      title: "Royal Chettinad Mansions",
      text: "Plan a 3-day Sivaganga Chettinad heritage food tour for 14k with authentic spicy crab",
      badge: "Merchant Mansions"
    },
    {
      title: "Classic Kerala Circuit",
      text: "Plan a 3-day Kerala trip for 15,000 with waterfalls and local food",
      badge: "Munnar Classic"
    }
  ];

  const handleSelectHub = (hub: typeof tnTourismHubs[0]) => {
    setSelectedHub(hub.title);
    setPrompt(hub.promptText);
    setDestination(hub.dest);
    setFoodPreference(hub.food);
    setInterests(hub.interests);
    handleParseText(hub.promptText);
  };

  const handleSelectSample = (sampleText: string) => {
    setPrompt(sampleText);
    handleParseText(sampleText);
  };

  const handleParseText = async (textToParse: string) => {
    if (!onParsePrompt) return;
    try {
      setIsParsing(true);
      const res = await onParsePrompt(textToParse);
      if (res) {
        if (res.destination) setDestination(res.destination);
        if (res.duration_days) setDurationDays(res.duration_days);
        if (res.budget) setBudget(res.budget);
        if (res.budget_tier) setBudgetTier(res.budget_tier);
        if (res.number_of_travelers) setTravelers(res.number_of_travelers);
        if (res.interests && res.interests.length > 0) setInterests(res.interests);
        if (res.food_preference) setFoodPreference(res.food_preference);
        if (res.hotel_preference) setHotelPreference(res.hotel_preference);
        if (res.travel_pace) setTravelPace(res.travel_pace);
        if (res.transport_preference) setTransportPreference(res.transport_preference);
      }
    } catch (e) {
      console.error("NLP parser note:", e);
    } finally {
      setIsParsing(false);
    }
  };

  const toggleInterest = (interest: string) => {
    if (interests.includes(interest)) {
      if (interests.length > 1) {
        setInterests(interests.filter(i => i !== interest));
      }
    } else {
      setInterests([...interests, interest]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const structuredProfile: PreferenceProfile = {
      destination,
      duration_days: durationDays,
      number_of_travelers: travelers,
      budget,
      currency: "INR",
      interests,
      disliked_categories: [],
      travel_pace: travelPace,
      food_preference: foodPreference,
      hotel_preference: hotelPreference,
      transport_preference: transportPreference,
      max_daily_travel_hours: 4.0,
      free_text_request: prompt
    };
    onGenerate(prompt, structuredProfile);
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-8 sm:py-12">
      {/* Hero Headline */}
      <div className="text-center space-y-3 mb-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
          <Sparkles className="h-3.5 w-3.5" />
          <span>IEEE ICUIS 2025 Granular 38-District Tourism Framework</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
          Granular Tamil Nadu Travel, <br />
          <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
            Customized District by District.
          </span>
        </h1>
        <p className="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto">
          Natural-language preference extraction for all 38 districts of Tamil Nadu, 
          mountain ghat transit buffers (~26 km/h), authentic regional cuisines, and verified operating hours.
        </p>
      </div>

      {/* Major TN Tourism Hub Quick Chips */}
      <div className="mb-6 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <Compass className="h-3.5 w-3.5 text-emerald-400" />
            <span>Featured Tamil Nadu Tourism Hubs</span>
          </span>
          <span className="text-[11px] text-slate-500">Click to auto-configure route</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
          {tnTourismHubs.map((hub) => {
            const Icon = hub.icon;
            const isSelected = selectedHub === hub.title;
            return (
              <button
                key={hub.id}
                type="button"
                onClick={() => handleSelectHub(hub)}
                className={`p-2.5 rounded-xl text-left border transition-all flex flex-col justify-between ${
                  isSelected
                    ? "bg-emerald-950/40 border-emerald-500 text-white shadow-md shadow-emerald-500/20 ring-1 ring-emerald-500/50"
                    : "bg-slate-900/80 hover:bg-slate-800/80 border-slate-800 text-slate-300 hover:border-slate-700"
                }`}
              >
                <div className="flex items-center gap-1.5 mb-1">
                  <Icon className={`h-3.5 w-3.5 shrink-0 ${isSelected ? "text-emerald-400" : "text-slate-400"}`} />
                  <span className="text-xs font-bold leading-tight line-clamp-1">{hub.title}</span>
                </div>
                <span className="text-[10px] text-slate-400 line-clamp-1">{hub.badge}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Search Bar Form */}
      <form onSubmit={handleSubmit} className="bg-slate-900/90 border border-slate-800 rounded-2xl shadow-2xl p-4 sm:p-6 backdrop-blur-md">
        <div className="relative">
          <div className="flex items-center gap-3 bg-slate-950 border border-slate-700/80 rounded-xl px-4 py-3 focus-within:border-emerald-500 focus-within:ring-2 focus-within:ring-emerald-500/20 transition-all">
            <Sparkles className="h-5 w-5 text-emerald-400 shrink-0" />
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g. Plan a 3-day Coimbatore and Ooty trip for 15,000 with Kongu food and tea"
              className="w-full bg-transparent text-slate-100 placeholder-slate-500 text-sm sm:text-base focus:outline-none"
            />
            {onParsePrompt && (
              <button
                type="button"
                onClick={() => handleParseText(prompt)}
                disabled={isParsing}
                className="hidden sm:inline-flex items-center gap-1 px-3 py-1 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg border border-slate-700 transition-colors shrink-0"
              >
                {isParsing ? "Extracting..." : "Auto-Parse"}
              </button>
            )}
          </div>
        </div>

        {/* Example Prompt Chips */}
        <div className="mt-4 flex flex-wrap items-center gap-2">
          <span className="text-xs text-slate-500 font-medium">Sample queries:</span>
          {samplePrompts.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectSample(sample.text)}
              className="text-xs px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-emerald-950/40 text-slate-300 hover:text-emerald-300 border border-slate-700/60 hover:border-emerald-500/30 transition-all flex items-center gap-1.5"
            >
              <span>{sample.title}</span>
              <span className="text-[10px] text-slate-500">({sample.badge})</span>
            </button>
          ))}
        </div>

        {/* Structured Fallback Filter Toggle */}
        <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between">
          <button
            type="button"
            onClick={() => setShowStructured(!showStructured)}
            className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1.5 transition-colors"
          >
            <SlidersHorizontal className="h-3.5 w-3.5" />
            <span>{showStructured ? "Hide Detailed Constraints" : "Customize Detailed Constraints (Districts, Budget, Pace, Cuisine)"}</span>
            {showStructured ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
          </button>

          {/* Quick summary badges */}
          <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400">
            <span className="px-2 py-0.5 rounded bg-slate-800 text-emerald-300 border border-slate-700">{destination}</span>
            <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300">{durationDays} Days</span>
            <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300">₹{budget.toLocaleString()}</span>
          </div>
        </div>

        {/* Structured Form Panel (Collapsible) */}
        {showStructured && (
          <div className="mt-4 p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-4 animate-fadeIn">
            {/* Row 1: Destination & Duration */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="text-xs font-medium text-slate-400 flex items-center gap-1 mb-1.5">
                  <MapPin className="h-3.5 w-3.5 text-emerald-400" /> State / Region
                </label>
                <div className="grid grid-cols-3 gap-1.5">
                  {["Tamil Nadu", "Kerala", "Goa"].map((dest) => (
                    <button
                      key={dest}
                      type="button"
                      onClick={() => setDestination(dest)}
                      className={`px-2 py-2 rounded-lg text-xs font-semibold transition-all border text-center ${
                        destination.includes(dest)
                          ? "bg-emerald-600 text-white border-emerald-500 shadow-sm shadow-emerald-500/30"
                          : "bg-slate-900 text-slate-400 border-slate-700 hover:bg-slate-800"
                      }`}
                    >
                      {dest}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400 flex items-center gap-1 mb-1.5">
                  <Calendar className="h-3.5 w-3.5 text-emerald-400" /> Duration (Days): <span className="text-emerald-400 font-bold ml-1">{durationDays}</span>
                </label>
                <input
                  type="range"
                  min={1}
                  max={7}
                  value={durationDays}
                  onChange={(e) => setDurationDays(parseInt(e.target.value))}
                  className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500 mt-2"
                />
                <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                  <span>1 Day</span>
                  <span>3 Days (Standard)</span>
                  <span>7 Days (Grand Circuit)</span>
                </div>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400 flex items-center gap-1 mb-1.5">
                  <Users className="h-3.5 w-3.5 text-emerald-400" /> Travelers
                </label>
                <div className="grid grid-cols-4 gap-1">
                  {[1, 2, 4, 6].map((num) => (
                    <button
                      key={num}
                      type="button"
                      onClick={() => setTravelers(num)}
                      className={`py-2 rounded-lg text-xs font-semibold border ${
                        travelers === num
                          ? "bg-emerald-600 text-white border-emerald-500"
                          : "bg-slate-900 text-slate-400 border-slate-700 hover:bg-slate-800"
                      }`}
                    >
                      {num} {num === 1 ? 'Solo' : (num === 2 ? 'Pair' : 'Pax')}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Row 2: Budget & Budget Tier */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-slate-800/80">
              <div>
                <label className="text-xs font-medium text-slate-400 flex items-center gap-1 mb-1.5">
                  <IndianRupee className="h-3.5 w-3.5 text-emerald-400" /> Budget Ceiling (INR)
                </label>
                <input
                  type="number"
                  step="1000"
                  min="2000"
                  max="200000"
                  value={budget}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value) || 0;
                    setBudget(val);
                    if (val < 18000) setBudgetTier("Budget");
                    else if (val <= 35000) setBudgetTier("Moderate");
                    else setBudgetTier("Luxury");
                  }}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400 mb-1.5 block">Budget Tier</label>
                <div className="grid grid-cols-3 gap-2">
                  {["Budget", "Moderate", "Luxury"].map((tier) => (
                    <button
                      key={tier}
                      type="button"
                      onClick={() => {
                        setBudgetTier(tier);
                        if (tier === "Budget" && budget > 18000) setBudget(15000);
                        if (tier === "Moderate" && (budget < 18000 || budget > 35000)) setBudget(25000);
                        if (tier === "Luxury" && budget < 35000) setBudget(45000);
                      }}
                      className={`px-2 py-2 rounded-lg text-xs font-semibold border ${
                        budgetTier === tier
                          ? "bg-emerald-600 text-white border-emerald-500"
                          : "bg-slate-900 text-slate-400 border-slate-700 hover:bg-slate-800"
                      }`}
                    >
                      {tier}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Row 3: Interests Badges */}
            <div className="pt-2 border-t border-slate-800/80">
              <label className="text-xs font-medium text-slate-400 mb-1.5 block">
                Target Interests & Experiences (Multi-Select)
              </label>
              <div className="flex flex-wrap gap-2">
                {availableInterests.map((interest) => {
                  const selected = interests.includes(interest);
                  return (
                    <button
                      key={interest}
                      type="button"
                      onClick={() => toggleInterest(interest)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all border ${
                        selected
                          ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
                          : "bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800"
                      }`}
                    >
                      {selected && <Check className="h-3 w-3 text-emerald-400" />}
                      <span>{interest}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Row 4: Travel Pace, Hotel & Food Preferences */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-slate-800/80">
              <div>
                <label className="text-[11px] font-medium text-slate-400 mb-1 block">Travel Pace</label>
                <select
                  value={travelPace}
                  onChange={(e) => setTravelPace(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                >
                  <option value="Relaxed pace">Relaxed pace (1-2 POIs/day)</option>
                  <option value="Moderate pace">Moderate pace (2-3 POIs/day)</option>
                  <option value="Fast pace">Fast pace (3-4 POIs/day)</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] font-medium text-slate-400 mb-1 block">Stay Preference</label>
                <select
                  value={hotelPreference}
                  onChange={(e) => setHotelPreference(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                >
                  <option value="Budget Hotel">Budget Hotel (~₹1,500/night)</option>
                  <option value="Homestay">Authentic District Homestay</option>
                  <option value="Luxury Resort">Luxury Heritage/Hill Resort</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] font-medium text-slate-400 mb-1 block">Authentic Culinary Flavor</label>
                <select
                  value={foodPreference}
                  onChange={(e) => setFoodPreference(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                >
                  <option value="Kongu Nadu Traditional">Kongu Nadu Traditional (Coimbatore/Erode)</option>
                  <option value="Nilgiri Highland Tea & Bakes">Nilgiri Tea & Bakery (Ooty Varkey)</option>
                  <option value="Madurai Traditional & Tiffin">Madurai Traditional (Jigarthanda & Tiffin)</option>
                  <option value="Chettinad Spicy Traditional">Chettinad Spicy Traditional (Karaikudi)</option>
                  <option value="Traditional Chola Nadu Tiffin">Chola Delta & Kumbakonam Kaapi</option>
                  <option value="Pure Vegetarian">Pure Vegetarian (Bhavan / Mess)</option>
                  <option value="Seafood Specialties">Coastal Seafood Catch</option>
                  <option value="Local Food">Authentic Regional Benchmark</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* CTA Generate Button */}
        <div className="mt-6">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 px-6 rounded-xl font-bold text-sm sm:text-base text-slate-950 bg-gradient-to-r from-emerald-400 via-teal-300 to-emerald-500 hover:from-emerald-300 hover:to-teal-400 transition-all shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {isLoading ? (
              <>
                <div className="h-5 w-5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                <span>Sequencing District Route & Mountain Buffers...</span>
              </>
            ) : (
              <>
                <Compass className="h-5 w-5 text-slate-950" />
                <span>Generate Smart Personalized Itinerary</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
