# TRIAL AI — MVP v1 Baseline Freeze Document

**Tag:** `trial-ai-mvp-v1-qa-passed`  
**Version:** 1.0.0-mvp  
**Freeze Date:** October 2, 2026  
**Status:** Stable Functional Baseline (QA Passed)  

---

## 1. Overview
This document freezes the initial working MVP checkpoint for **TRIAL AI — AI-Powered Smart Tourist Guide**. All core functionalities have passed end-to-end QA validation across desktop and mobile viewports.

---

## 2. Current Features
1. **Interactive Landing Experience:**
   - Visual presentation grounded in IEEE ICUIS 2025 and ICARC 2026.
   - Quick one-click "Demo Login" for pre-filled evaluation (`Priya & Rahul`).
2. **Personalized Preference Extraction & Constraint Form:**
   - Multi-factor configuration: destination (Kerala / Goa), duration (3 days), travelers (2), budget cap (₹15,000), interests (Waterfalls, Trekking), local food, budget hotel, and moderate pace.
3. **IEEE Normalized Multi-Feature Recommendation Engine:**
   - Objective composite scoring:
     $$\text{Score} = 0.30 \cdot \text{Pref} + 0.15 \cdot \text{Context} + 0.15 \cdot \text{Dist} + 0.15 \cdot \text{Quality} + 0.15 \cdot \text{Budget} + 0.10 \cdot \text{Schedule}$$
   - Explainable AI decomposition with individual component bars and rationale strings.
4. **Deterministic Feasible Itinerary Engine:**
   - Zero-overlap scheduling with strictly enforced venue opening hours.
   - Transit time estimates (~32 km/h mountain speed) with scenic route notes.
   - Integrated meal windows (Lunch at 12:45, Dinner at 19:45).
   - Integrated base camp hotel check-in at Green Valley Nature Homestay.
5. **Predictive Budget Engine:**
   - Category-wise itemized breakdown (Accommodation, Food, Transport, Activities, Buffer).
   - Uncertainty forecasting intervals (Min, Expected, Max).
   - Real-time budget variance alert (Expected ₹13,800 fits within ₹15,000 cap with ₹1,200 surplus).
6. **Geospatial Route Map:**
   - Leaflet + OpenStreetMap interactive container with colored pins, polyline route trails, and popups.
7. **Local Hotel & Food Integrations:**
   - Curated budget stays and authentic Kerala eateries (Rapsy Restaurant, Guru's Mess, ClayHut, Tea Tales).
8. **Offline Survivability Module:**
   - Complete JSON offline package generation and download.
   - Offline mode simulation with cached itinerary and Kerala emergency helplines.
9. **Persistent Saved Trips & Feedback:**
   - LocalStorage and in-memory trip persistence.
   - Interactive 5-star rating and comment submission.

---

## 3. Tests Passed
- **Backend Engine Unit Tests (`pytest backend/tests/test_engines.py`):**
  - `test_recommendation_scoring_weights`: **PASSED** (Weights sum to 1.0)
  - `test_poi_scoring_affinity`: **PASSED** (Waterfall affinity validated)
  - `test_budget_engine_calculation`: **PASSED** (₹15k cap feasibility validated)
  - `test_itinerary_feasibility_no_overlap`: **PASSED** (Zero time overlap validated)
- **E2E Playwright Automation Suite (`tests/e2e_qa_journey.py`):**
  - Desktop Viewport (1280×850): **13 / 13 PASSED**
  - Mobile Viewport (390×844): **7 / 7 PASSED**
  - Total E2E Tests: **20 / 20 PASSED (100%)**
  - Console Errors: **0**

---

## 4. Known Limitations in MVP v1
1. **Map Engine Fallback:** Default interactive map uses Leaflet + OpenStreetMap tiles rather than live Google Maps JavaScript API keys.
2. **Pricing Telemetry:** Uses verified regional benchmark tariffs rather than live OTA booking APIs.
3. **Database Mode:** Uses fast in-memory store and browser local storage; Firestore integration is mocked for demo reliability.

---

## 5. Files Included in Checkpoint
- `backend/main.py`: FastAPI server with REST API routes & static mount.
- `backend/models.py`: Pydantic data schemas.
- `backend/recommendation_engine.py`: IEEE normalized multi-feature scorer.
- `backend/itinerary_engine.py`: Deterministic constraint route solver.
- `backend/budget_engine.py`: Predictive budgeting engine with uncertainty ranges.
- `backend/data/kerala_seed.json`: Kerala POIs, budget hotels, and eateries dataset.
- `backend/data/goa_seed.json`: Secondary seed dataset.
- `backend/tests/test_engines.py`: Unit test harness.
- `frontend/public/index.html`: Complete reactive responsive frontend.
- `frontend/package.json`: Vite and React TypeScript dependencies.
- `frontend/src/types.ts`: TypeScript interfaces.
- `tests/e2e_qa_journey.py`: Playwright automated QA test script.
- `docs/final-qa-report.md`: Complete QA validation report.
- `docs/screenshots/`: 20 visual screenshots across desktop and mobile.
- `.gitignore`: Ignored artifact paths.
- `.env.example`: Environment variable template.

---

## 6. Next Development Phase
- **Phase 2:** Visual polish for final-year project presentation (typography, badge aesthetics, AI natural-language prompt input, enhanced score cards, timeline styling).
- **Phase 3:** Pluggable Map Provider architecture (`mock`, `leaflet`, `google`).
- **Phase 4:** Dedicated Research-to-Module visible mapping section.
- **Phase 5:** Real model evaluation harness (`/evaluation` dashboard comparing baseline vs personalized scoring).
- **Phase 6:** Complete project thesis and defense documentation.
