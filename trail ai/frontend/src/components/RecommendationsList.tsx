import React from 'react';
import { ScoredRecommendation } from '../types';
import { Sparkles, Star, MapPin, IndianRupee, Clock, Check } from 'lucide-react';

interface RecommendationsListProps {
  recommendations: ScoredRecommendation[];
}

export const RecommendationsList: React.FC<RecommendationsListProps> = ({ recommendations }) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">IEEE Multi-Feature POI Rankings</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Ranked via normalized multi-objective scoring function with explainable sub-attribute breakdowns
          </p>
        </div>
        <span className="text-xs text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20 font-bold">
          {recommendations.length} Candidate POIs Ranked
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recommendations.map((rec, idx) => (
          <div
            key={rec.item_id}
            className="p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-all space-y-3"
          >
            {/* Header */}
            <div className="flex items-start justify-between gap-2">
              <div>
                <div className="flex items-center gap-2">
                  <span className="h-5 w-5 rounded-full bg-emerald-500 text-slate-950 font-bold text-xs flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <h3 className="text-sm font-bold text-white">{rec.name}</h3>
                </div>
                <div className="text-[11px] text-emerald-400 mt-1 font-semibold">
                  {rec.category}
                </div>
              </div>

              {/* Composite Score Pill */}
              <div className="text-right">
                <div className="text-xs font-bold text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded-lg border border-emerald-500/30 font-mono">
                  Score: {rec.scores.total_score.toFixed(3)}
                </div>
              </div>
            </div>

            {/* Explainable Rationale */}
            <div className="text-xs text-slate-300 bg-slate-950/70 p-2.5 rounded-lg border border-slate-800/80 flex items-start gap-2">
              <Sparkles className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
              <span className="text-[11px] leading-relaxed italic">{rec.primary_explanation}</span>
            </div>

            {/* Sub-Attribute Breakdown Progress Bars */}
            <div className="space-y-1.5 pt-1 text-[10px]">
              <div className="flex items-center justify-between text-slate-400">
                <span>Preference Match (w=0.30)</span>
                <span className="font-mono text-slate-200">{(rec.scores.preference_match * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500" style={{ width: `${rec.scores.preference_match * 100}%` }} />
              </div>

              <div className="flex items-center justify-between text-slate-400">
                <span>Quality & Review Rating (w=0.15)</span>
                <span className="font-mono text-slate-200">{(rec.scores.quality_score * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-teal-400" style={{ width: `${rec.scores.quality_score * 100}%` }} />
              </div>

              <div className="flex items-center justify-between text-slate-400">
                <span>Budget & Entry Fit (w=0.15)</span>
                <span className="font-mono text-slate-200">{(rec.scores.budget_fit * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-cyan-400" style={{ width: `${rec.scores.budget_fit * 100}%` }} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
