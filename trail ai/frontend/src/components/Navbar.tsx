import React from 'react';
import { Compass, Sparkles, Wifi, WifiOff, Bookmark, HelpCircle } from 'lucide-react';
import { User } from '../types';

interface NavbarProps {
  user: User | null;
  isOffline: boolean;
  onToggleOffline: () => void;
  activeScreen: string;
  onNavigate: (screen: string) => void;
  savedTripsCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  user,
  isOffline,
  onToggleOffline,
  activeScreen,
  onNavigate,
  savedTripsCount
}) => {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <div 
          onClick={() => onNavigate('landing')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <Compass className="h-6 w-6 text-white animate-spin-slow" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold tracking-tight text-white">Trail<span className="text-emerald-400">AI</span></span>
              <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                IEEE MVP
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">Smart Personalized Tourism Planner</p>
          </div>
        </div>

        {/* Center / Right Navigation Controls */}
        <div className="flex items-center gap-2 sm:gap-4">
          {/* Saved Trips Shortcut */}
          <button
            onClick={() => onNavigate('saved')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors ${
              activeScreen === 'saved'
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                : 'text-slate-300 hover:bg-slate-800'
            }`}
          >
            <Bookmark className="h-4 w-4" />
            <span className="hidden sm:inline">Saved Trips</span>
            {savedTripsCount > 0 && (
              <span className="h-4 min-w-4 px-1 rounded-full bg-emerald-500 text-slate-950 text-[10px] font-bold flex items-center justify-center">
                {savedTripsCount}
              </span>
            )}
          </button>

          {/* Offline Mode Toggle */}
          <button
            onClick={onToggleOffline}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all border ${
              isOffline
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/30 shadow-sm shadow-amber-500/20'
                : 'text-slate-400 hover:text-slate-200 border-slate-800 hover:bg-slate-900'
            }`}
            title={isOffline ? "Currently in Offline Cached Mode" : "Switch to Offline Simulation Mode"}
          >
            {isOffline ? (
              <>
                <WifiOff className="h-3.5 w-3.5 text-amber-400 animate-pulse" />
                <span>Offline Active</span>
              </>
            ) : (
              <>
                <Wifi className="h-3.5 w-3.5 text-emerald-400" />
                <span className="hidden md:inline">Online Engine</span>
              </>
            )}
          </button>

          {/* User Profile / Demo Login */}
          <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
            <div className="h-8 w-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-semibold text-emerald-400">
              PR
            </div>
            <div className="hidden md:block text-left">
              <div className="text-xs font-medium text-slate-200">{user?.name || "Priya & Rahul"}</div>
              <div className="text-[10px] text-slate-500">Demo Traveler Profile</div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
