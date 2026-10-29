import React from 'react';
import { OfflinePackage, Hotel } from '../types';
import { 
  X, Download, ShieldAlert, Phone, MapPin, 
  CheckCircle2, Bed, WifiOff, FileText 
} from 'lucide-react';

interface OfflineModalProps {
  isOpen: boolean;
  onClose: () => void;
  offlinePackage?: OfflinePackage;
  hotel?: Hotel;
}

export const OfflineModal: React.FC<OfflineModalProps> = ({
  isOpen,
  onClose,
  offlinePackage,
  hotel
}) => {
  if (!isOpen) return null;

  const handleDownloadJson = () => {
    if (!offlinePackage) return;
    const blob = new Blob([JSON.stringify(offlinePackage, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `trail-ai-${offlinePackage.destination.toLowerCase()}-offline.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5 animate-scaleIn">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
              <WifiOff className="h-5 w-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white">Offline Resilience Pack</h2>
              <p className="text-xs text-slate-400">Essential navigation, stays, and emergency helplines</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Offline Status Note */}
        <div className="p-3.5 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-300 text-xs flex items-start gap-2.5">
          <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <div className="font-bold">Trip Cached in Local Storage</div>
            <div className="text-[11px] text-emerald-400/80 mt-0.5">
              Coordinates, scheduled stops, and verified tariffs remain accessible even in remote valleys without cellular coverage.
            </div>
          </div>
        </div>

        {/* Emergency Contacts */}
        <div className="space-y-2">
          <div className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
            <ShieldAlert className="h-4 w-4 text-rose-400" />
            <span>Emergency Helplines ({offlinePackage?.destination || "Kerala"})</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {(offlinePackage?.emergency_contacts || [
              { name: "Kerala Police Tourist Helpline", phone: "1800-425-4747", type: "Police" },
              { name: "Medical Emergency Ambulance", phone: "108", type: "Medical" },
              { name: "Disaster Management Helpline", phone: "1077", type: "Emergency" },
              { name: "Munnar Tourist Info Office", phone: "+91-4865-231516", type: "Tourism" }
            ]).map((contact, idx) => (
              <div 
                key={idx}
                className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between text-xs"
              >
                <div>
                  <div className="font-semibold text-slate-200">{contact.name}</div>
                  <div className="text-[10px] text-slate-500">{contact.type}</div>
                </div>
                <a 
                  href={`tel:${contact.phone}`}
                  className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-400 font-mono font-bold text-[11px] flex items-center gap-1"
                >
                  <Phone className="h-3 w-3" />
                  <span>{contact.phone}</span>
                </a>
              </div>
            ))}
          </div>
        </div>

        {/* Basecamp Stay Summary */}
        {hotel && (
          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5">
            <div className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
              <Bed className="h-4 w-4 text-blue-400" />
              <span>Basecamp Hotel Address & Coordinates</span>
            </div>
            <div className="text-xs text-white font-semibold">{hotel.name}</div>
            <div className="text-[11px] text-slate-400 flex items-center gap-1">
              <MapPin className="h-3 w-3 text-slate-500 shrink-0" />
              <span>{hotel.address}</span>
            </div>
            <div className="text-[11px] text-slate-500 font-mono">
              GPS: {hotel.lat.toFixed(4)}° N, {hotel.lng.toFixed(4)}° E
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="pt-2 flex flex-col sm:flex-row gap-2">
          <button
            onClick={handleDownloadJson}
            className="flex-1 py-2.5 px-4 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors flex items-center justify-center gap-2"
          >
            <Download className="h-4 w-4" />
            <span>Download Offline JSON Package</span>
          </button>
          <button
            onClick={onClose}
            className="py-2.5 px-4 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
