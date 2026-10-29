import React, { useState, useEffect } from 'react';
import { 
  Trip, PreferenceProfile, Hotel, POI, FoodPlace, DailyPlan, BudgetSummary, User 
} from './types';
import { Navbar } from './components/Navbar';
import { NaturalLanguageSearch } from './components/NaturalLanguageSearch';
import { GenerationModal } from './components/GenerationModal';
import { TimelineView } from './components/TimelineView';
import { MapView } from './components/MapView';
import { BudgetCard } from './components/BudgetCard';
import { RefinementDrawer } from './components/RefinementDrawer';
import { RecommendationsList } from './components/RecommendationsList';
import { OfflineModal } from './components/OfflineModal';
import { 
  Compass, Map, Calendar, IndianRupee, Sparkles, SlidersHorizontal, 
  Bookmark, BookmarkCheck, Download, RefreshCw, AlertCircle, Trash2, ArrowLeft, Plus 
} from 'lucide-react';

const API_BASE = window.location.origin;

export const App: React.FC = () => {
  // Navigation & View state
  const [activeScreen, setActiveScreen] = useState<'landing' | 'planner' | 'saved'>('landing');
  const [activeView, setActiveView] = useState<'itinerary' | 'map' | 'budget' | 'recommendations'>('itinerary');
  const [selectedDay, setSelectedDay] = useState<number>(1);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [isOffline, setIsOffline] = useState<boolean>(false);

  // Modals & Drawers
  const [isRefinementOpen, setIsRefinementOpen] = useState<boolean>(false);
  const [refinementAction, setRefinementAction] = useState<string>("swap_hotel");
  const [refinementDay, setRefinementDay] = useState<number>(1);
  const [refinementStopId, setRefinementStopId] = useState<string | undefined>(undefined);
  const [isOfflineModalOpen, setIsOfflineModalOpen] = useState<boolean>(false);

  // Data states
  const [currentTrip, setCurrentTrip] = useState<Trip | null>(null);
  const [savedTrips, setSavedTrips] = useState<Trip[]>([]);
  const [availableHotels, setAvailableHotels] = useState<Hotel[]>([]);
  const [availablePois, setAvailablePois] = useState<POI[]>([]);
  const [user, setUser] = useState<User | null>({
    user_id: "user_demo_traveler",
    name: "Priya & Rahul",
    email: "travelers@example.com",
    is_demo: true
  });

  // Load initial saved trips & destination metadata on startup
  useEffect(() => {
    try {
      const cached = localStorage.getItem('trail_ai_saved_trips');
      if (cached) {
        setSavedTrips(JSON.parse(cached));
      }
      // Check last generated trip cache
      const lastTrip = localStorage.getItem('trail_ai_last_trip');
      if (lastTrip) {
        const parsed = JSON.parse(lastTrip);
        setCurrentTrip(parsed);
      }
    } catch (e) {
      console.warn("Storage restore note:", e);
    }

    // Check online status
    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      setIsOffline(true);
    }

    // Fetch available POIs and hotels from API for default destination
    fetchHotelsAndPois("Kerala");
  }, []);

  const fetchHotelsAndPois = async (dest: string) => {
    try {
      const [hotelsRes, poisRes] = await Promise.all([
        fetch(`${API_BASE}/destinations/${dest}/hotels`).then(r => r.ok ? r.json() : []),
        fetch(`${API_BASE}/pois?destination=${dest}`).then(r => r.ok ? r.json() : [])
      ]);
      if (hotelsRes && hotelsRes.length > 0) setAvailableHotels(hotelsRes);
      if (poisRes && poisRes.length > 0) setAvailablePois(poisRes);
    } catch (e) {
      console.log("Using cached candidate seed data:", e);
    }
  };

  // 1. Natural Language Parse API
  const handleParsePrompt = async (promptText: string) => {
    try {
      const res = await fetch(`${API_BASE}/trip/parse`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: promptText })
      });
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.warn("Parse fallback note:", e);
    }
    return null;
  };

  // 2. Generate Trip Pipeline
  const handleGenerateTrip = async (promptText: string, structuredData?: PreferenceProfile) => {
    setIsGenerating(true);
    try {
      const payload: any = {};
      if (structuredData) {
        payload.profile = structuredData;
      } else {
        payload.prompt = promptText;
      }
      payload.user_id = user?.user_id || "user_demo_traveler";

      const res = await fetch(`${API_BASE}/trip/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error(`Generation failed: ${res.statusText}`);
      }

      const trip: Trip = await res.json();
      setCurrentTrip(trip);
      setSelectedDay(1);
      setActiveScreen('planner');
      setActiveView('itinerary');

      // Update available stays and candidate POIs for this destination
      fetchHotelsAndPois(trip.profile.destination);

      // Persist in localStorage for offline resilience
      try {
        localStorage.setItem('trail_ai_last_trip', JSON.stringify(trip));
      } catch (e) {}

    } catch (err) {
      console.error("Trip generation error:", err);
      alert("Unable to reach online engine. Switching to local offline cache.");
      setIsOffline(true);
    } finally {
      setTimeout(() => {
        setIsGenerating(false);
      }, 900);
    }
  };

  // 3. Trip Refinement Local Handler
  const handleRefineTrip = async (action: string, payload: any) => {
    if (!currentTrip) return;

    try {
      const refineReq = {
        trip_id: currentTrip.trip_id,
        action,
        ...payload
      };

      const res = await fetch(`${API_BASE}/trip/refine`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(refineReq)
      });

      if (!res.ok) {
        throw new Error(`Refinement error: ${res.statusText}`);
      }

      const result = await res.json();
      if (result.success && result.trip) {
        setCurrentTrip(result.trip);
        try {
          localStorage.setItem('trail_ai_last_trip', JSON.stringify(result.trip));
        } catch (e) {}
      }
    } catch (e) {
      console.error("Refine API error:", e);
    }
  };

  // 4. Quick Remove POI
  const handleRemoveStop = async (dayNumber: number, stopId: string) => {
    if (!currentTrip) return;
    await handleRefineTrip("remove_poi", { day_number: dayNumber, poi_id: stopId });
  };

  // 5. Save & Bookmark Trip
  const isTripSaved = currentTrip && savedTrips.some(t => t.trip_id === currentTrip.trip_id);

  const handleToggleSaveTrip = () => {
    if (!currentTrip) return;
    let updated: Trip[];
    if (isTripSaved) {
      updated = savedTrips.filter(t => t.trip_id !== currentTrip.trip_id);
    } else {
      updated = [currentTrip, ...savedTrips];
    }
    setSavedTrips(updated);
    try {
      localStorage.setItem('trail_ai_saved_trips', JSON.stringify(updated));
    } catch (e) {}
  };

  const handleDeleteSavedTrip = (id: string) => {
    const updated = savedTrips.filter(t => t.trip_id !== id);
    setSavedTrips(updated);
    try {
      localStorage.setItem('trail_ai_saved_trips', JSON.stringify(updated));
    } catch (e) {}
  };

  const openRefinementDrawer = (action: string, dayNumber: number = 1, stopId?: string) => {
    setRefinementAction(action);
    setRefinementDay(dayNumber);
    setRefinementStopId(stopId);
    setIsRefinementOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 font-sans selection:bg-emerald-500 selection:text-white">
      {/* Top Navigation */}
      <Navbar
        user={user}
        isOffline={isOffline}
        onToggleOffline={() => setIsOffline(!isOffline)}
        activeScreen={activeScreen}
        onNavigate={(screen) => setActiveScreen(screen as any)}
        savedTripsCount={savedTrips.length}
      />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col">
        {/* SCREEN 1: LANDING & SEARCH BAR */}
        {activeScreen === 'landing' && (
          <div className="flex-1 flex flex-col justify-center py-6 sm:py-12">
            <NaturalLanguageSearch
              onGenerate={handleGenerateTrip}
              isLoading={isGenerating}
              onParsePrompt={handleParsePrompt}
            />

            {/* Quick jump to active trip if available */}
            {currentTrip && (
              <div className="max-w-md mx-auto text-center mt-6">
                <button
                  onClick={() => setActiveScreen('planner')}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 border border-emerald-500/30 text-emerald-400 text-xs font-bold hover:bg-slate-800 transition-colors"
                >
                  <Compass className="h-4 w-4" />
                  <span>Resume Current {currentTrip.profile.destination} Itinerary</span>
                </button>
              </div>
            )}
          </div>
        )}

        {/* SCREEN 2: ACTIVE PLANNER DASHBOARD */}
        {activeScreen === 'planner' && currentTrip && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full space-y-6 animate-fadeIn">
            {/* Top Itinerary Summary Bar */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-emerald-400 bg-emerald-950/60 px-2.5 py-0.5 rounded border border-emerald-500/20">
                    {currentTrip.profile.destination} Circuit
                  </span>
                  <span className="text-xs text-slate-400">•</span>
                  <span className="text-xs text-slate-400">{currentTrip.profile.duration_days} Days / {currentTrip.profile.number_of_travelers} Travelers</span>
                </div>
                <h1 className="text-xl sm:text-2xl font-extrabold text-white mt-1">
                  {currentTrip.profile.destination} Smart Itinerary
                </h1>
                <p className="text-xs text-slate-400 mt-0.5">
                  Basecamp: <span className="text-slate-200 font-semibold">{currentTrip.selected_hotel?.name}</span> • Pace: {currentTrip.profile.travel_pace}
                </p>
              </div>

              {/* Action Toolbar */}
              <div className="flex flex-wrap items-center gap-2 shrink-0">
                <button
                  onClick={() => openRefinementDrawer("swap_hotel", selectedDay)}
                  className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center gap-1.5 transition-colors"
                >
                  <SlidersHorizontal className="h-3.5 w-3.5 text-emerald-400" />
                  <span>Refine Trip</span>
                </button>

                <button
                  onClick={() => setIsOfflineModalOpen(true)}
                  className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center gap-1.5 transition-colors"
                >
                  <Download className="h-3.5 w-3.5 text-amber-400" />
                  <span>Offline Pack</span>
                </button>

                <button
                  onClick={handleToggleSaveTrip}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold border flex items-center gap-1.5 transition-colors ${
                    isTripSaved
                      ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
                      : "bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-700"
                  }`}
                >
                  {isTripSaved ? <BookmarkCheck className="h-3.5 w-3.5 text-emerald-400" /> : <Bookmark className="h-3.5 w-3.5" />}
                  <span>{isTripSaved ? "Saved" : "Save Trip"}</span>
                </button>

                <button
                  onClick={() => setActiveScreen('landing')}
                  className="px-3 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
                >
                  Plan Another
                </button>
              </div>
            </div>

            {/* Dashboard Views Navigation Tabs */}
            <div className="flex border-b border-slate-800 gap-2 sm:gap-6 text-sm font-bold overflow-x-auto no-scrollbar">
              <button
                onClick={() => setActiveView('itinerary')}
                className={`pb-3 px-1 border-b-2 transition-all flex items-center gap-2 shrink-0 ${
                  activeView === 'itinerary'
                    ? "border-emerald-500 text-emerald-400"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Calendar className="h-4 w-4" />
                <span>Day-by-Day Itinerary</span>
              </button>

              <button
                onClick={() => setActiveView('map')}
                className={`pb-3 px-1 border-b-2 transition-all flex items-center gap-2 shrink-0 ${
                  activeView === 'map'
                    ? "border-emerald-500 text-emerald-400"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Map className="h-4 w-4" />
                <span>Interactive Route Map</span>
              </button>

              <button
                onClick={() => setActiveView('budget')}
                className={`pb-3 px-1 border-b-2 transition-all flex items-center gap-2 shrink-0 ${
                  activeView === 'budget'
                    ? "border-emerald-500 text-emerald-400"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <IndianRupee className="h-4 w-4" />
                <span>Budget Tracker</span>
                {currentTrip.budget_summary?.within_budget && (
                  <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                )}
              </button>

              <button
                onClick={() => setActiveView('recommendations')}
                className={`pb-3 px-1 border-b-2 transition-all flex items-center gap-2 shrink-0 ${
                  activeView === 'recommendations'
                    ? "border-emerald-500 text-emerald-400"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Sparkles className="h-4 w-4" />
                <span>IEEE Scoring Breakdown</span>
              </button>
            </div>

            {/* Active Sub-View Body */}
            <div>
              {activeView === 'itinerary' && (
                <TimelineView
                  dailyPlans={currentTrip.daily_plans}
                  profile={currentTrip.profile}
                  selectedDay={selectedDay}
                  onSelectDay={setSelectedDay}
                  onOpenRefinement={openRefinementDrawer}
                  onRemoveStop={handleRemoveStop}
                />
              )}

              {activeView === 'map' && (
                <MapView
                  dailyPlans={currentTrip.daily_plans}
                  selectedDay={selectedDay}
                  onSelectDay={setSelectedDay}
                  isOffline={isOffline}
                />
              )}

              {activeView === 'budget' && currentTrip.budget_summary && (
                <BudgetCard budgetSummary={currentTrip.budget_summary} />
              )}

              {activeView === 'recommendations' && (
                <RecommendationsList recommendations={currentTrip.recommendations} />
              )}
            </div>
          </div>
        )}

        {/* SCREEN 3: SAVED TRIPS LIST */}
        {activeScreen === 'saved' && (
          <div className="max-w-4xl mx-auto px-4 py-8 w-full space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h1 className="text-2xl font-bold text-white">Saved Itineraries</h1>
                <p className="text-xs text-slate-400 mt-1">Locally persisted trips ready for offline travel</p>
              </div>
              <button
                onClick={() => setActiveScreen('landing')}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors flex items-center gap-1.5"
              >
                <Plus className="h-3.5 w-3.5" />
                <span>Plan New Trip</span>
              </button>
            </div>

            {savedTrips.length === 0 ? (
              <div className="text-center py-16 bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-3">
                <Bookmark className="h-10 w-10 text-slate-600 mx-auto" />
                <h3 className="text-base font-bold text-slate-300">No Saved Trips Yet</h3>
                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                  When you plan a trip, click the "Save Trip" button in the planner toolbar to keep it permanently available here.
                </p>
                <button
                  onClick={() => setActiveScreen('landing')}
                  className="mt-4 px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 text-white"
                >
                  Create Your First Trip
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {savedTrips.map(trip => (
                  <div
                    key={trip.trip_id}
                    className="p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-500/20">
                          {trip.profile.destination}
                        </span>
                        <span className="text-xs text-slate-400">{trip.profile.duration_days} Days</span>
                        <span className="text-xs text-slate-400">•</span>
                        <span className="text-xs text-slate-400">₹{Math.round(trip.profile.budget).toLocaleString()}</span>
                      </div>
                      <h3 className="text-base font-bold text-white mt-1">
                        {trip.profile.destination} ({trip.profile.interests.join(", ")})
                      </h3>
                      <p className="text-xs text-slate-400 mt-0.5">
                        Stay: {trip.selected_hotel?.name} • Created {new Date(trip.created_at).toLocaleDateString()}
                      </p>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <button
                        onClick={() => {
                          setCurrentTrip(trip);
                          setSelectedDay(1);
                          setActiveScreen('planner');
                        }}
                        className="px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors"
                      >
                        Open Itinerary
                      </button>
                      <button
                        onClick={() => handleDeleteSavedTrip(trip.trip_id)}
                        className="p-2 rounded-xl text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition-colors"
                        title="Delete saved trip"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      {/* Generation Progress Modal */}
      <GenerationModal isOpen={isGenerating} />

      {/* Refinement Drawer */}
      {currentTrip && (
        <RefinementDrawer
          isOpen={isRefinementOpen}
          onClose={() => setIsRefinementOpen(false)}
          tripId={currentTrip.trip_id}
          initialAction={refinementAction}
          targetDay={refinementDay}
          targetStopId={refinementStopId}
          currentHotel={currentTrip.selected_hotel}
          availableHotels={availableHotels}
          availablePois={availablePois}
          profile={currentTrip.profile}
          onRefine={handleRefineTrip}
        />
      )}

      {/* Offline Resilience Modal */}
      {currentTrip && (
        <OfflineModal
          isOpen={isOfflineModalOpen}
          onClose={() => setIsOfflineModalOpen(false)}
          offlinePackage={currentTrip.offline_package}
          hotel={currentTrip.selected_hotel}
        />
      )}
    </div>
  );
};

export default App;
