import React, { useEffect, useRef, useState } from 'react';
import { DailyPlan, ItineraryStop } from '../types';
import L from 'leaflet';
import { MapPin, Navigation, Compass, AlertCircle, WifiOff } from 'lucide-react';

interface MapViewProps {
  dailyPlans: DailyPlan[];
  selectedDay: number;
  onSelectDay: (day: number) => void;
  isOffline: boolean;
}

export const MapView: React.FC<MapViewProps> = ({
  dailyPlans,
  selectedDay,
  onSelectDay,
  isOffline
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markersLayerRef = useRef<L.LayerGroup | null>(null);
  const routeLayerRef = useRef<L.Polyline | null>(null);

  const [tileError, setTileError] = useState(false);

  const currentPlan = dailyPlans.find(p => p.day_number === selectedDay) || dailyPlans[0];
  const stops = currentPlan?.stops || [];

  useEffect(() => {
    if (!mapContainerRef.current) return;

    // Center coordinates: use first stop or default to Kerala center
    const defaultCenter: [number, number] = stops.length > 0
      ? [stops[0].lat, stops[0].lng]
      : [10.0889, 77.0595];

    // Initialize Leaflet map instance once
    if (!mapInstanceRef.current) {
      const map = L.map(mapContainerRef.current, {
        center: defaultCenter,
        zoom: 12,
        zoomControl: true
      });

      const tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; OpenStreetMap contributors'
      });

      tileLayer.on('tileerror', () => {
        setTileError(true);
      });

      tileLayer.addTo(map);

      markersLayerRef.current = L.layerGroup().addTo(map);
      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;
    if (markersLayerRef.current) {
      markersLayerRef.current.clearLayers();
    }
    if (routeLayerRef.current) {
      routeLayerRef.current.remove();
      routeLayerRef.current = null;
    }

    if (stops.length > 0) {
      const latLngs: L.LatLngExpression[] = [];

      stops.forEach((stop, idx) => {
        const isHotel = stop.type === "hotel_checkin";
        const isFood = stop.type.startsWith("food_");
        const pinColor = isHotel ? "#3b82f6" : (isFood ? "#f59e0b" : "#10b981");

        // Custom HTML pin icon
        const customIcon = L.divIcon({
          className: 'custom-poi-marker',
          html: `
            <div style="
              background-color: ${pinColor};
              color: white;
              width: 32px;
              height: 32px;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              font-weight: 800;
              font-size: 13px;
              border: 2px solid #0f172a;
              box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            ">
              ${idx + 1}
            </div>
          `,
          iconSize: [32, 32],
          iconAnchor: [16, 16],
          popupAnchor: [0, -18]
        });

        const marker = L.marker([stop.lat, stop.lng], { icon: customIcon });

        const popupContent = `
          <div style="font-family: inherit; font-size: 12px; line-height: 1.4; padding: 4px;">
            <div style="font-weight: 800; color: #10b981; margin-bottom: 2px;">Stop ${idx + 1}: ${stop.name}</div>
            <div style="color: #94a3b8; font-size: 11px; margin-bottom: 4px;">${stop.category} • ${stop.start_time} - ${stop.end_time}</div>
            <div style="color: #cbd5e1; margin-bottom: 6px;">${stop.description}</div>
            <div style="display: flex; justify-content: space-between; font-weight: bold; color: #38bdf8; font-size: 11px;">
              <span>Cost: ₹${Math.round(stop.cost_for_group)}</span>
              <span>Coords: ${stop.lat.toFixed(3)}, ${stop.lng.toFixed(3)}</span>
            </div>
          </div>
        `;

        marker.bindPopup(popupContent);
        markersLayerRef.current?.addLayer(marker);
        latLngs.push([stop.lat, stop.lng]);
      });

      // Draw chronological route line between consecutive stops
      if (latLngs.length > 1) {
        const polyline = L.polyline(latLngs, {
          color: '#10b981',
          weight: 4,
          opacity: 0.8,
          dashArray: '8, 8',
          lineCap: 'round'
        }).addTo(map);

        routeLayerRef.current = polyline;
        map.fitBounds(polyline.getBounds(), { padding: [50, 50] });
      } else if (latLngs.length === 1) {
        map.setView(latLngs[0], 13);
      }
    }

    // Force map container layout refresh
    setTimeout(() => {
      map.invalidateSize();
    }, 200);

  }, [dailyPlans, selectedDay, stops]);

  return (
    <div className="space-y-4">
      {/* Day Selector Buttons & Legend */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900 border border-slate-800 p-3 rounded-xl">
        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar">
          {dailyPlans.map(plan => (
            <button
              key={plan.day_number}
              onClick={() => onSelectDay(plan.day_number)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold border shrink-0 transition-colors ${
                selectedDay === plan.day_number
                  ? "bg-emerald-600 text-white border-emerald-500"
                  : "bg-slate-950 text-slate-400 border-slate-800 hover:bg-slate-800 hover:text-slate-200"
              }`}
            >
              Day {plan.day_number} Route ({plan.stops.length} stops)
            </button>
          ))}
        </div>

        {/* Legend */}
        <div className="flex items-center gap-3 text-[11px] text-slate-400">
          <div className="flex items-center gap-1.5">
            <div className="h-3 w-3 rounded-full bg-blue-500" />
            <span>Stay</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="h-3 w-3 rounded-full bg-emerald-500" />
            <span>Attraction / POI</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="h-3 w-3 rounded-full bg-amber-500" />
            <span>Dining</span>
          </div>
        </div>
      </div>

      {/* Map Container */}
      <div className="relative w-full h-[450px] sm:h-[550px] rounded-2xl overflow-hidden border border-slate-800 shadow-2xl bg-slate-950">
        <div ref={mapContainerRef} className="w-full h-full" />

        {/* Offline / Tile Error Banner Overlay */}
        {(isOffline || tileError) && (
          <div className="absolute top-4 right-4 z-[1000] max-w-xs bg-slate-900/95 border border-amber-500/40 rounded-xl p-3 shadow-xl backdrop-blur-md">
            <div className="flex items-start gap-2.5">
              <WifiOff className="h-4 w-4 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <div className="text-xs font-bold text-amber-300">Offline Resilience Active</div>
                <div className="text-[11px] text-slate-400 mt-0.5">
                  Pre-cached GPS coordinates and route waypoints remain active. Background map tiles render from local browser cache.
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Chronological Waypoints Ribbon */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
        <div className="text-xs font-bold text-slate-300 mb-2 flex items-center gap-1.5">
          <Navigation className="h-3.5 w-3.5 text-emerald-400" />
          <span>Day {selectedDay} Waypoint Sequence</span>
        </div>
        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1">
          {stops.map((stop, idx) => (
            <React.Fragment key={stop.stop_id}>
              <div className="shrink-0 flex items-center gap-1.5 bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-lg text-xs">
                <span className="h-4 w-4 rounded-full bg-emerald-500 text-slate-950 font-bold text-[10px] flex items-center justify-center">
                  {idx + 1}
                </span>
                <span className="font-medium text-slate-200">{stop.name}</span>
                <span className="text-[10px] text-slate-500">({stop.start_time})</span>
              </div>
              {idx < stops.length - 1 && (
                <span className="text-slate-600 font-mono shrink-0">→</span>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
};
