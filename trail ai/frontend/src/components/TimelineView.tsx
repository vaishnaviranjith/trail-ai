import React, { useState } from 'react';
import { 
  DailyPlan, ItineraryStop, RouteSegment, PreferenceProfile 
} from '../types';
import { 
  Clock, MapPin, Navigation, IndianRupee, Sparkles, AlertCircle, 
  ChevronDown, ChevronUp, Trash2, RefreshCw, Plus, CheckCircle2, Bed, Utensils,
  Mountain, Compass
} from 'lucide-react';

interface TimelineViewProps {
  dailyPlans: DailyPlan[];
  profile: PreferenceProfile;
  selectedDay: number;
  onSelectDay: (day: number) => void;
  onOpenRefinement: (action: string, dayNumber?: number, stopId?: string) => void;
  onRemoveStop: (dayNumber: number, stopId: string) => void;
}

export const TimelineView: React.FC<TimelineViewProps> = ({
  dailyPlans,
  profile,
  selectedDay,
  onSelectDay,
  onOpenRefinement,
  onRemoveStop
}) => {
  const currentPlan = dailyPlans.find(p => p.day_number === selectedDay) || dailyPlans[0];

  // Helper to categorize stops into morning, afternoon, evening
  const categorizeStopsByBlock = (stops: ItineraryStop[]) => {
    const morning: ItineraryStop[] = [];
    const afternoon: ItineraryStop[] = [];
    const evening: ItineraryStop[] = [];

    stops.forEach(stop => {
      const startHour = parseInt(stop.start_time.split(":")[0]);
      if (startHour < 12) {
        morning.push(stop);
      } else if (startHour < 17) {
        afternoon.push(stop);
      } else {
        evening.push(stop);
      }
    });

    return { morning, afternoon, evening };
  };

  const { morning, afternoon, evening } = categorizeStopsByBlock(currentPlan?.stops || []);

  const [expandedBlocks, setExpandedBlocks] = useState<{ [key: string]: boolean }>({
    morning: true,
    afternoon: true,
    evening: true
  });

  const toggleBlock = (blockKey: string) => {
    setExpandedBlocks(prev => ({ ...prev, [blockKey]: !prev[blockKey] }));
  };

  return (
    <div className="space-y-6">
      {/* Day Selector Pills */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar">
          {dailyPlans.map(plan => (
            <button
              key={plan.day_number}
              onClick={() => onSelectDay(plan.day_number)}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all border shrink-0 ${
                selectedDay === plan.day_number
                  ? "bg-emerald-600 text-white border-emerald-500 shadow-md shadow-emerald-500/25"
                  : "bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800 hover:text-slate-200"
              }`}
            >
              Day {plan.day_number}
            </button>
          ))}
        </div>

        <button
          onClick={() => onOpenRefinement("add_poi", selectedDay)}
          className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5 transition-colors"
        >
          <Plus className="h-3.5 w-3.5" />
          <span>Add Stop to Day {selectedDay}</span>
        </button>
      </div>

      {/* Day Header & Metadata Card */}
      {currentPlan && (
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-lg">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                {currentPlan.theme}
              </span>
              <h2 className="text-lg sm:text-xl font-bold text-white mt-0.5">
                {currentPlan.title}
              </h2>
            </div>

            {/* Day Feasibility Badges */}
            <div className="flex flex-wrap items-center gap-2 text-xs">
              <span className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 flex items-center gap-1">
                <Clock className="h-3.5 w-3.5 text-emerald-400" />
                <span>{currentPlan.total_travel_time_minutes}m transit</span>
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 flex items-center gap-1">
                <Navigation className="h-3.5 w-3.5 text-teal-400" />
                <span>{currentPlan.total_distance_km} km</span>
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-semibold flex items-center gap-1">
                <IndianRupee className="h-3.5 w-3.5" />
                <span>₹{Math.round(currentPlan.day_cost).toLocaleString()}</span>
              </span>
            </div>
          </div>

          <div className="mt-3 pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-400">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0" />
              <span>Feasible zero-overlap circuit verified against daylight & operating hours.</span>
            </div>
            {currentPlan.route_segments?.some(s => s.is_ghat_route) && (
              <span className="px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 font-semibold flex items-center gap-1">
                <Mountain className="h-3 w-3" /> Mountain Ghat Corridor Active
              </span>
            )}
          </div>
        </div>
      )}

      {/* Timeline Blocks */}
      <div className="space-y-4">
        {/* Morning Block */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/60 overflow-hidden">
          <div 
            onClick={() => toggleBlock('morning')}
            className="flex items-center justify-between px-5 py-3.5 bg-slate-900/90 cursor-pointer hover:bg-slate-800/80 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <div className="h-2.5 w-2.5 rounded-full bg-amber-400 ring-4 ring-amber-400/20" />
              <span className="text-sm font-bold text-white">Morning Slot (08:30 – 12:30)</span>
              <span className="text-xs text-slate-400">({morning.length} {morning.length === 1 ? 'stop' : 'stops'})</span>
            </div>
            {expandedBlocks.morning ? <ChevronUp className="h-4 w-4 text-slate-400" /> : <ChevronDown className="h-4 w-4 text-slate-400" />}
          </div>

          {expandedBlocks.morning && (
            <div className="p-5 space-y-4">
              {morning.length === 0 ? (
                <div className="text-xs text-slate-500 py-3 text-center">No morning stops scheduled.</div>
              ) : (
                morning.map((stop) => (
                  <StopCard
                    key={stop.stop_id}
                    stop={stop}
                    dayNumber={selectedDay}
                    routeSegments={currentPlan?.route_segments || []}
                    onOpenRefinement={onOpenRefinement}
                    onRemoveStop={onRemoveStop}
                  />
                ))
              )}
            </div>
          )}
        </div>

        {/* Afternoon Block */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/60 overflow-hidden">
          <div 
            onClick={() => toggleBlock('afternoon')}
            className="flex items-center justify-between px-5 py-3.5 bg-slate-900/90 cursor-pointer hover:bg-slate-800/80 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <div className="h-2.5 w-2.5 rounded-full bg-emerald-400 ring-4 ring-emerald-400/20" />
              <span className="text-sm font-bold text-white">Afternoon Slot (12:30 – 17:00)</span>
              <span className="text-xs text-slate-400">({afternoon.length} {afternoon.length === 1 ? 'stop' : 'stops'})</span>
            </div>
            {expandedBlocks.afternoon ? <ChevronUp className="h-4 w-4 text-slate-400" /> : <ChevronDown className="h-4 w-4 text-slate-400" />}
          </div>

          {expandedBlocks.afternoon && (
            <div className="p-5 space-y-4">
              {afternoon.length === 0 ? (
                <div className="text-xs text-slate-500 py-3 text-center">No afternoon stops scheduled.</div>
              ) : (
                afternoon.map((stop) => (
                  <StopCard
                    key={stop.stop_id}
                    stop={stop}
                    dayNumber={selectedDay}
                    routeSegments={currentPlan?.route_segments || []}
                    onOpenRefinement={onOpenRefinement}
                    onRemoveStop={onRemoveStop}
                  />
                ))
              )}
            </div>
          )}
        </div>

        {/* Evening Block */}
        <div className="border border-slate-800 rounded-2xl bg-slate-900/60 overflow-hidden">
          <div 
            onClick={() => toggleBlock('evening')}
            className="flex items-center justify-between px-5 py-3.5 bg-slate-900/90 cursor-pointer hover:bg-slate-800/80 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <div className="h-2.5 w-2.5 rounded-full bg-indigo-400 ring-4 ring-indigo-400/20" />
              <span className="text-sm font-bold text-white">Evening & Dinner Slot (17:00 – 21:00)</span>
              <span className="text-xs text-slate-400">({evening.length} {evening.length === 1 ? 'stop' : 'stops'})</span>
            </div>
            {expandedBlocks.evening ? <ChevronUp className="h-4 w-4 text-slate-400" /> : <ChevronDown className="h-4 w-4 text-slate-400" />}
          </div>

          {expandedBlocks.evening && (
            <div className="p-5 space-y-4">
              {evening.length === 0 ? (
                <div className="text-xs text-slate-500 py-3 text-center">No evening stops scheduled.</div>
              ) : (
                evening.map((stop) => (
                  <StopCard
                    key={stop.stop_id}
                    stop={stop}
                    dayNumber={selectedDay}
                    routeSegments={currentPlan?.route_segments || []}
                    onOpenRefinement={onOpenRefinement}
                    onRemoveStop={onRemoveStop}
                  />
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Reusable Sub-Card for individual itinerary stop with connected Route Segment
interface StopCardProps {
  stop: ItineraryStop;
  dayNumber: number;
  routeSegments: RouteSegment[];
  onOpenRefinement: (action: string, dayNumber?: number, stopId?: string) => void;
  onRemoveStop: (dayNumber: number, stopId: string) => void;
}

const StopCard: React.FC<StopCardProps> = ({
  stop,
  dayNumber,
  routeSegments,
  onOpenRefinement,
  onRemoveStop
}) => {
  const isHotel = stop.type === "hotel_checkin";
  const isFood = stop.type.startsWith("food_");
  const nextSegment = routeSegments.find(s => s.from_name === stop.name);

  return (
    <div className="space-y-3">
      <div className="bg-slate-950/70 border border-slate-800/90 rounded-xl p-4 transition-all hover:border-slate-700 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
          {/* Left Side: Time, Badges, District & Title */}
          <div className="space-y-2 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-500/20">
                {stop.start_time} – {stop.end_time}
              </span>
              <span className="text-[11px] text-slate-400 font-medium">({stop.duration_minutes} mins)</span>
              
              {/* District Badge */}
              {stop.district && (
                <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/30">
                  <MapPin className="h-3 w-3 text-purple-400" /> {stop.district}
                </span>
              )}

              {/* Stop Category Badge */}
              {isHotel ? (
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 flex items-center gap-1">
                  <Bed className="h-3 w-3" /> Basecamp Stay
                </span>
              ) : isFood ? (
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center gap-1">
                  <Utensils className="h-3 w-3" /> {stop.category}
                </span>
              ) : (
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {stop.category}
                </span>
              )}

              {/* Operating Hours */}
              {stop.opening_time && stop.closing_time && (
                <span className="inline-flex items-center gap-1 text-[11px] text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                  <Clock className="h-3 w-3 text-slate-400" /> Hours: {stop.opening_time} – {stop.closing_time}
                </span>
              )}
            </div>

            <h3 className="text-base font-bold text-white leading-snug">
              {stop.name}
            </h3>

            <p className="text-xs text-slate-400 leading-relaxed">
              {stop.description}
            </p>

            {/* District Context Description */}
            {stop.district_description && (
              <div className="flex items-center gap-1.5 text-[11px] text-purple-300/90 bg-purple-950/20 px-2.5 py-1 rounded-lg border border-purple-500/20">
                <MapPin className="h-3 w-3 text-purple-400 shrink-0" />
                <span><strong className="text-purple-200">{stop.district} Region:</strong> {stop.district_description}</span>
              </div>
            )}

            {/* Authentic Food Specialties (for dining stops) */}
            {stop.food_specialties && stop.food_specialties.length > 0 && (
              <div className="flex flex-wrap items-center gap-1.5 pt-0.5">
                <span className="text-[11px] font-semibold text-amber-300 flex items-center gap-1">
                  <Utensils className="h-3 w-3" /> Authentic Specialties:
                </span>
                {stop.food_specialties.map(specialty => (
                  <span
                    key={specialty}
                    className="text-[10px] font-medium px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20"
                  >
                    {specialty}
                  </span>
                ))}
              </div>
            )}

            {/* Explainable AI Snippet */}
            <div className="flex items-center gap-1.5 text-[11px] text-emerald-400/90 bg-emerald-950/20 px-2 py-1 rounded-lg border border-emerald-500/10">
              <Sparkles className="h-3 w-3 shrink-0" />
              <span className="italic line-clamp-1">{stop.recommendation_reason}</span>
            </div>
          </div>

          {/* Right Side: Cost & Local Refinement Actions */}
          <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-start gap-2 shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-800">
            <div className="text-xs font-bold text-slate-200">
              {stop.cost_for_group === 0 ? (
                <span className="text-emerald-400">Free Entry</span>
              ) : (
                <span>₹{Math.round(stop.cost_for_group).toLocaleString()}</span>
              )}
            </div>

            <div className="flex items-center gap-1">
              {isHotel ? (
                <button
                  onClick={() => onOpenRefinement("swap_hotel", dayNumber, stop.stop_id)}
                  className="px-2.5 py-1 text-[11px] font-medium bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-lg flex items-center gap-1 transition-colors"
                  title="Swap Basecamp Hotel"
                >
                  <RefreshCw className="h-3 w-3" />
                  <span>Swap Stay</span>
                </button>
              ) : (
                <>
                  <button
                    onClick={() => onOpenRefinement("swap_poi", dayNumber, stop.stop_id)}
                    className="p-1.5 text-slate-400 hover:text-emerald-400 hover:bg-slate-800 rounded-lg transition-colors"
                    title="Swap Stop with Alternative"
                  >
                    <RefreshCw className="h-3.5 w-3.5" />
                  </button>
                  <button
                    onClick={() => onRemoveStop(dayNumber, stop.stop_id)}
                    className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors"
                    title="Remove Stop"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Transit Connector between Stops */}
      {nextSegment && (
        <div className="ml-4 pl-4 border-l-2 border-dashed border-slate-800 py-1">
          <div className={`rounded-xl p-3 text-xs border ${
            nextSegment.is_ghat_route
              ? "bg-amber-950/30 border-amber-500/30 text-amber-200"
              : "bg-slate-900/70 border-slate-800 text-slate-300"
          }`}>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                {nextSegment.is_ghat_route ? (
                  <span className="p-1 rounded-md bg-amber-500/20 text-amber-300">
                    <Mountain className="h-4 w-4" />
                  </span>
                ) : (
                  <span className="p-1 rounded-md bg-slate-800 text-emerald-400">
                    <Navigation className="h-4 w-4" />
                  </span>
                )}
                <div>
                  <span className="font-bold text-white">
                    {nextSegment.is_ghat_route ? (nextSegment.corridor_name || "Mountain Ghat Corridor") : "Transit Segment"}
                  </span>
                  <div className="text-[11px] text-slate-400 flex items-center gap-2">
                    <span>{nextSegment.distance_km} km</span>
                    <span>•</span>
                    <span>~{nextSegment.travel_time_minutes} mins</span>
                    {nextSegment.hairpin_bends ? (
                      <>
                        <span>•</span>
                        <span className="text-amber-400 font-semibold">{nextSegment.hairpin_bends} Hairpin Bends</span>
                      </>
                    ) : null}
                    {nextSegment.buffer_minutes ? (
                      <>
                        <span>•</span>
                        <span className="text-amber-300">+{nextSegment.buffer_minutes}m buffer</span>
                      </>
                    ) : null}
                  </div>
                </div>
              </div>

              {nextSegment.is_ghat_route && (
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">
                  Ghat Speed: ~26 km/h
                </span>
              )}
            </div>

            {nextSegment.scenic_note && (
              <p className="mt-1.5 text-[11px] text-slate-400 italic">
                {nextSegment.scenic_note}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
