import React, { useState, useEffect } from 'react';
import { 
  Hotel, POI, PreferenceProfile 
} from '../types';
import { 
  X, RefreshCw, Bed, Plus, Sliders, Check, 
  MapPin, Star, Clock, Mountain
} from 'lucide-react';

interface RefinementDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  tripId: string;
  initialAction?: string;
  targetDay?: number;
  targetStopId?: string;
  currentHotel?: Hotel;
  availableHotels: Hotel[];
  availablePois: POI[];
  profile: PreferenceProfile;
  onRefine: (action: string, payload: any) => Promise<void>;
}

export const RefinementDrawer: React.FC<RefinementDrawerProps> = ({
  isOpen,
  onClose,
  tripId,
  initialAction = "swap_hotel",
  targetDay = 1,
  targetStopId,
  currentHotel,
  availableHotels,
  availablePois,
  profile,
  onRefine
}) => {
  const [activeTab, setActiveTab] = useState<string>(initialAction);
  const [selectedDay, setSelectedDay] = useState<number>(targetDay);
  const [selectedSlot, setSelectedSlot] = useState<string>("afternoon");
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [selectedDistrict, setSelectedDistrict] = useState<string>("All");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Constraint editing states
  const [pace, setPace] = useState<string>(profile.travel_pace);
  const [transport, setTransport] = useState<string>(profile.transport_preference);
  const [budgetVal, setBudgetVal] = useState<number>(profile.budget);

  useEffect(() => {
    setActiveTab(initialAction);
    setSelectedDay(targetDay);
  }, [initialAction, targetDay]);

  if (!isOpen) return null;

  const categories = ["All", "Waterfalls", "Trekking", "Nature & Viewpoints", "Heritage & Culture"];

  // Dynamically extract unique districts from available POIs
  const uniqueDistricts = Array.from(
    new Set(availablePois.map(p => p.district).filter(Boolean) as string[])
  ).sort();
  const districtOptions = ["All", ...uniqueDistricts];

  const filteredPois = availablePois.filter(p => {
    if (selectedDistrict !== "All" && p.district !== selectedDistrict) return false;
    if (selectedCategory === "All") return true;
    if (selectedCategory === "Waterfalls") return p.category.toLowerCase().includes("waterfall");
    if (selectedCategory === "Trekking") return p.category.toLowerCase().includes("trek");
    if (selectedCategory === "Nature & Viewpoints") return p.tags.includes("nature") || p.tags.includes("scenic");
    if (selectedCategory === "Heritage & Culture") return p.tags.includes("heritage") || p.tags.includes("culture");
    return true;
  });

  const handleSelectHotel = async (hotelId: string) => {
    setIsLoading(true);
    try {
      await onRefine("swap_hotel", { hotel_id: hotelId });
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddPoi = async (poiId: string) => {
    setIsLoading(true);
    try {
      if (initialAction === "swap_poi" && targetStopId) {
        await onRefine("swap_poi", {
          day_number: selectedDay,
          poi_id: targetStopId,
          target_poi_id: poiId
        });
      } else {
        await onRefine("add_poi", {
          day_number: selectedDay,
          target_poi_id: poiId,
          slot: selectedSlot
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateConstraints = async () => {
    setIsLoading(true);
    try {
      await onRefine("update_constraints", {
        profile_updates: {
          travel_pace: pace,
          transport_preference: transport,
          budget: budgetVal
        }
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/80 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-lg bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col h-full animate-slideInRight">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <RefreshCw className="h-4 w-4 text-emerald-400" />
            <h2 className="text-base font-bold text-white">Interactive Refinement</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Tab Switcher */}
        <div className="px-5 pt-3 border-b border-slate-800 flex items-center gap-2">
          <button
            onClick={() => setActiveTab("swap_hotel")}
            className={`pb-2.5 px-2 text-xs font-bold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === "swap_hotel"
                ? "border-emerald-500 text-emerald-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <Bed className="h-3.5 w-3.5" />
            <span>Swap Hotel</span>
          </button>

          <button
            onClick={() => setActiveTab("add_poi")}
            className={`pb-2.5 px-2 text-xs font-bold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === "add_poi" || activeTab === "swap_poi"
                ? "border-emerald-500 text-emerald-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <Plus className="h-3.5 w-3.5" />
            <span>{activeTab === "swap_poi" ? "Swap Stop" : "Add Stop"}</span>
          </button>

          <button
            onClick={() => setActiveTab("update_constraints")}
            className={`pb-2.5 px-2 text-xs font-bold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === "update_constraints"
                ? "border-emerald-500 text-emerald-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <Sliders className="h-3.5 w-3.5" />
            <span>Constraints</span>
          </button>
        </div>

        {/* Drawer Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {isLoading && (
            <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
              <div className="h-4 w-4 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
              <span>Applying localized recalculations without full reload...</span>
            </div>
          )}

          {/* TAB 1: SWAP HOTEL */}
          {activeTab === "swap_hotel" && (
            <div className="space-y-4">
              <p className="text-xs text-slate-400">
                Choose a basecamp stay. Itinerary morning departures and accommodation budget will update automatically.
              </p>

              <div className="space-y-3">
                {availableHotels.map(hotel => {
                  const isCurrent = currentHotel?.id === hotel.id;
                  return (
                    <div
                      key={hotel.id}
                      className={`p-4 rounded-xl border transition-all ${
                        isCurrent
                          ? "bg-emerald-950/30 border-emerald-500/50"
                          : "bg-slate-950/60 border-slate-800 hover:border-slate-700"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="space-y-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <h3 className="text-sm font-bold text-white">{hotel.name}</h3>
                            {hotel.district && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/30 flex items-center gap-1">
                                <MapPin className="h-2.5 w-2.5" /> {hotel.district}
                              </span>
                            )}
                            {isCurrent && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400">
                                Current Stay
                              </span>
                            )}
                          </div>
                          <div className="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
                            <span className="text-emerald-400 font-semibold">{hotel.category}</span>
                            <span>•</span>
                            <span className="flex items-center gap-0.5 text-amber-400">
                              <Star className="h-3 w-3 fill-amber-400" /> {hotel.rating}
                            </span>
                            <span>•</span>
                            <span>{hotel.room_type}</span>
                          </div>
                          <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">{hotel.description}</p>
                        </div>

                        <div className="text-right shrink-0">
                          <div className="text-sm font-bold text-white font-mono">
                            ₹{Math.round(hotel.price_per_night)}
                          </div>
                          <div className="text-[10px] text-slate-500">per night</div>
                        </div>
                      </div>

                      {!isCurrent && (
                        <div className="mt-3 pt-3 border-t border-slate-800/80">
                          <button
                            onClick={() => handleSelectHotel(hotel.id)}
                            disabled={isLoading}
                            className="w-full py-2 px-3 rounded-lg text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors flex items-center justify-center gap-1.5 disabled:opacity-50"
                          >
                            <Check className="h-3.5 w-3.5" />
                            <span>Select as Base Camp</span>
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TAB 2: ADD / SWAP POI */}
          {(activeTab === "add_poi" || activeTab === "swap_poi") && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-medium text-slate-400 mb-1 block">Target Day</label>
                  <select
                    value={selectedDay}
                    onChange={(e) => setSelectedDay(parseInt(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200"
                  >
                    {[1, 2, 3, 4, 5].slice(0, profile.duration_days).map(d => (
                      <option key={d} value={d}>Day {d}</option>
                    ))}
                  </select>
                </div>

                {activeTab !== "swap_poi" && (
                  <div>
                    <label className="text-xs font-medium text-slate-400 mb-1 block">Slot</label>
                    <select
                      value={selectedSlot}
                      onChange={(e) => setSelectedSlot(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200"
                    >
                      <option value="morning">Morning (10:00)</option>
                      <option value="afternoon">Afternoon (14:30)</option>
                      <option value="evening">Sunset (17:30)</option>
                    </select>
                  </div>
                )}
              </div>

              {/* District Filter (if multiple districts present) */}
              {districtOptions.length > 2 && (
                <div>
                  <label className="text-[11px] font-semibold text-slate-400 mb-1 flex items-center gap-1">
                    <MapPin className="h-3 w-3 text-purple-400" /> Filter by District
                  </label>
                  <div className="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto no-scrollbar">
                    {districtOptions.map(district => (
                      <button
                        key={district}
                        onClick={() => setSelectedDistrict(district)}
                        className={`px-2.5 py-0.5 rounded-md text-[11px] font-medium transition-colors ${
                          selectedDistrict === district
                            ? "bg-purple-600 text-white shadow-sm"
                            : "bg-slate-950 text-slate-400 border border-slate-800 hover:text-slate-200"
                        }`}
                      >
                        {district}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Category Filter Chips */}
              <div>
                <label className="text-[11px] font-semibold text-slate-400 mb-1 block">Category</label>
                <div className="flex flex-wrap gap-1.5">
                  {categories.map(cat => (
                    <button
                      key={cat}
                      onClick={() => setSelectedCategory(cat)}
                      className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors ${
                        selectedCategory === cat
                          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                          : "bg-slate-950 text-slate-400 border border-slate-800 hover:bg-slate-850"
                      }`}
                    >
                      {cat}
                    </button>
                  ))}
                </div>
              </div>

              {/* POI Cards */}
              <div className="space-y-3">
                {filteredPois.map(poi => (
                  <div
                    key={poi.id}
                    className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-slate-700 space-y-2 transition-all"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="space-y-1">
                        <div className="flex flex-wrap items-center gap-1.5">
                          <h4 className="text-xs font-bold text-white">{poi.name}</h4>
                          {poi.district && (
                            <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 flex items-center gap-0.5">
                              <MapPin className="h-2.5 w-2.5" /> {poi.district}
                            </span>
                          )}
                          {poi.is_mountain_route && (
                            <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20 flex items-center gap-0.5">
                              <Mountain className="h-2.5 w-2.5" /> Hill Station
                            </span>
                          )}
                        </div>

                        <div className="text-[11px] text-slate-400 flex flex-wrap items-center gap-1.5">
                          <span className="text-emerald-400">{poi.category}</span>
                          <span>•</span>
                          <span className="flex items-center gap-0.5 text-amber-400">
                            <Star className="h-3 w-3 fill-amber-400" /> {poi.rating}
                          </span>
                          <span>•</span>
                          <span>{poi.typical_duration_minutes}m visit</span>
                          {poi.opening_time && poi.closing_time && (
                            <>
                              <span>•</span>
                              <span className="flex items-center gap-0.5 text-slate-400">
                                <Clock className="h-2.5 w-2.5" /> {poi.opening_time} – {poi.closing_time}
                              </span>
                            </>
                          )}
                        </div>
                      </div>

                      <div className="text-right shrink-0">
                        <span className="text-xs font-bold text-slate-200">
                          {poi.entry_fee_per_person === 0 ? "Free" : `₹${poi.entry_fee_per_person}/pax`}
                        </span>
                      </div>
                    </div>

                    <p className="text-[11px] text-slate-400 line-clamp-2">{poi.description}</p>

                    <div className="pt-2 border-t border-slate-800/80 flex justify-end">
                      <button
                        onClick={() => handleAddPoi(poi.id)}
                        disabled={isLoading}
                        className="py-1 px-3 rounded-lg text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors flex items-center gap-1 disabled:opacity-50"
                      >
                        <Plus className="h-3.5 w-3.5" />
                        <span>{activeTab === "swap_poi" ? "Swap with this Stop" : "Add to Schedule"}</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: CONSTRAINTS */}
          {activeTab === "update_constraints" && (
            <div className="space-y-4">
              <div>
                <label className="text-xs font-medium text-slate-300 mb-1.5 block">Travel Pace</label>
                <div className="grid grid-cols-3 gap-2">
                  {["Relaxed pace", "Moderate pace", "Fast pace"].map(p => (
                    <button
                      key={p}
                      onClick={() => setPace(p)}
                      className={`p-2 rounded-lg text-xs font-semibold border ${
                        pace === p
                          ? "bg-emerald-600 text-white border-emerald-500"
                          : "bg-slate-950 text-slate-400 border-slate-800"
                      }`}
                    >
                      {p.replace(" pace", "")}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 mb-1.5 block">Transport Preference</label>
                <select
                  value={transport}
                  onChange={(e) => setTransport(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200"
                >
                  <option value="Local Taxi / Cab">Local Taxi / Dedicated Cab</option>
                  <option value="Self-drive Scooter / Bike">Self-drive Scooter / Bike</option>
                  <option value="Public Transit">Public Transit / Bus</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 mb-1.5 block">Budget Ceiling (INR)</label>
                <input
                  type="number"
                  step="1000"
                  value={budgetVal}
                  onChange={(e) => setBudgetVal(parseFloat(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100"
                />
              </div>

              <div className="pt-4 border-t border-slate-800">
                <button
                  onClick={handleUpdateConstraints}
                  disabled={isLoading}
                  className="w-full py-2.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors flex items-center justify-center gap-2"
                >
                  <Check className="h-4 w-4" />
                  <span>Update Constraints & Recalculate</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
