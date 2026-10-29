import React from 'react';
import { BudgetSummary } from '../types';
import { 
  IndianRupee, CheckCircle2, AlertTriangle, TrendingDown, 
  TrendingUp, ShieldCheck, Info, Sparkles 
} from 'lucide-react';

interface BudgetCardProps {
  budgetSummary: BudgetSummary;
}

export const BudgetCard: React.FC<BudgetCardProps> = ({ budgetSummary }) => {
  const percentUsed = Math.min(100, Math.round((budgetSummary.total_expected_cost / budgetSummary.total_budget) * 100));
  const isSurplus = budgetSummary.within_budget;
  const remaining = budgetSummary.budget_remaining;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 sm:p-6 shadow-xl space-y-6">
      {/* Header & Feasibility Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white">Dynamic Budget Projection</h2>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              IEEE Predictive Model
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Itemized breakdown with min/expected/max uncertainty forecasting
          </p>
        </div>

        {/* Status Pill */}
        <div className={`px-3 py-1.5 rounded-xl border flex items-center gap-2 ${
          isSurplus 
            ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400" 
            : "bg-rose-500/10 border-rose-500/30 text-rose-400"
        }`}>
          {isSurplus ? (
            <>
              <CheckCircle2 className="h-4 w-4 text-emerald-400" />
              <div className="text-xs font-bold">Within Budget Ceiling</div>
            </>
          ) : (
            <>
              <AlertTriangle className="h-4 w-4 text-rose-400" />
              <div className="text-xs font-bold">Exceeds Budget Ceiling</div>
            </>
          )}
        </div>
      </div>

      {/* Main Budget Bar Meter */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-3">
        <div className="flex items-end justify-between">
          <div>
            <div className="text-xs text-slate-400">Total Projected Spending</div>
            <div className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-1">
              <span>₹{Math.round(budgetSummary.total_expected_cost).toLocaleString()}</span>
              <span className="text-xs text-slate-500 font-normal self-end mb-1">
                (Range: ₹{Math.round(budgetSummary.min_cost).toLocaleString()} – ₹{Math.round(budgetSummary.max_cost).toLocaleString()})
              </span>
            </div>
          </div>

          <div className="text-right">
            <div className="text-xs text-slate-400">Budget Limit</div>
            <div className="text-lg sm:text-xl font-bold text-slate-300">
              ₹{Math.round(budgetSummary.total_budget).toLocaleString()}
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
          <div 
            className={`h-full transition-all duration-500 ${
              percentUsed > 95 ? "bg-amber-500" : (percentUsed > 100 ? "bg-rose-500" : "bg-gradient-to-r from-emerald-500 to-teal-400")
            }`}
            style={{ width: `${percentUsed}%` }}
          />
        </div>

        {/* Footer remaining stats */}
        <div className="flex items-center justify-between text-xs pt-1">
          <div className="text-slate-400">
            <span className="font-semibold text-slate-200">{percentUsed}%</span> of total budget allocated
          </div>
          <div className={`font-semibold flex items-center gap-1 ${
            isSurplus ? "text-emerald-400" : "text-rose-400"
          }`}>
            {isSurplus ? (
              <>
                <TrendingDown className="h-3.5 w-3.5" />
                <span>₹{Math.round(remaining).toLocaleString()} surplus buffer</span>
              </>
            ) : (
              <>
                <TrendingUp className="h-3.5 w-3.5" />
                <span>₹{Math.round(Math.abs(remaining)).toLocaleString()} over budget</span>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Category-Wise Itemized Breakdown */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-slate-200">Category-Wise Expenditure Breakdown</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {budgetSummary.items.map((item, idx) => (
            <div 
              key={idx}
              className="bg-slate-950/70 border border-slate-800 rounded-xl p-3.5 space-y-2 hover:border-slate-700 transition-colors"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white">{item.category}</span>
                <span className="text-xs font-extrabold text-emerald-400 font-mono">
                  ₹{Math.round(item.expected_cost).toLocaleString()}
                </span>
              </div>

              <div className="text-[11px] font-medium text-slate-300">{item.label}</div>
              <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">{item.details}</p>

              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-500">
                <span>Range: ₹{Math.round(item.min_cost)} – ₹{Math.round(item.max_cost)}</span>
                <span className="text-slate-400 italic">{item.price_source}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
