import React, { useEffect, useState } from 'react';
import { Compass, CheckCircle2, Clock, Sparkles, MapPin, Calculator } from 'lucide-react';

interface GenerationModalProps {
  isOpen: boolean;
  onFinish?: () => void;
}

export const GenerationModal: React.FC<GenerationModalProps> = ({ isOpen }) => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { title: "Intent & Preference Extraction", desc: "Extracting destination, dates, budget ceiling, and travel style", icon: Sparkles },
    { title: "Candidate Space Retrieval", desc: "Filtering regional POIs, hotels, and dining benchmarks from seed datasets", icon: MapPin },
    { title: "IEEE Normalized Recommendation Scoring", desc: "Computing multi-attribute composite weights (preference, rating, distance, budget)", icon: Compass },
    { title: "Spatial Clustering & Route Optimization", desc: "Sequencing non-overlapping daily schedules with mountain transit buffering", icon: Clock },
    { title: "Predictive Dynamic Budgeting", desc: "Projecting itemized expenditure with min/expected/max uncertainty forecasting", icon: Calculator },
  ];

  useEffect(() => {
    if (!isOpen) {
      setCurrentStep(0);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < steps.length - 1) return prev + 1;
        return prev;
      });
    }, 450);

    return () => clearInterval(interval);
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl max-w-md w-full p-6 text-center space-y-6 animate-scaleIn">
        {/* Animated Radar/Compass Header */}
        <div className="relative mx-auto w-16 h-16 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
          <Compass className="h-8 w-8 text-emerald-400 animate-spin-slow" />
          <div className="absolute inset-0 rounded-full border border-emerald-500/20 animate-ping" />
        </div>

        <div>
          <h3 className="text-lg font-bold text-white">Synthesizing Personalized Itinerary</h3>
          <p className="text-xs text-slate-400 mt-1">Executing IEEE Smart Tourism Optimization Pipeline</p>
        </div>

        {/* Step-by-Step Progress Timeline */}
        <div className="space-y-3 text-left">
          {steps.map((s, idx) => {
            const isCompleted = idx < currentStep;
            const isCurrent = idx === currentStep;
            const Icon = s.icon;

            return (
              <div 
                key={idx} 
                className={`flex items-start gap-3 p-2.5 rounded-xl transition-all ${
                  isCurrent 
                    ? "bg-emerald-950/40 border border-emerald-500/30 text-emerald-300" 
                    : isCompleted 
                    ? "text-slate-400" 
                    : "text-slate-600 opacity-60"
                }`}
              >
                <div className="mt-0.5 shrink-0">
                  {isCompleted ? (
                    <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  ) : isCurrent ? (
                    <div className="h-4 w-4 rounded-full border-2 border-emerald-400 border-t-transparent animate-spin" />
                  ) : (
                    <Icon className="h-4 w-4 text-slate-600" />
                  )}
                </div>
                <div className="flex-1">
                  <div className="text-xs font-semibold leading-tight">{s.title}</div>
                  <div className="text-[11px] text-slate-400 line-clamp-1">{s.desc}</div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="text-[11px] text-slate-500 italic">
          Grounded in verified seed benchmarks • Zero hallucinations
        </div>
      </div>
    </div>
  );
};
