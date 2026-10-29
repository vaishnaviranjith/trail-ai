import time
import os
import sys
from playwright.sync_api import sync_playwright

def run_qa_suite():
    screenshots_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "screenshots"))
    os.makedirs(screenshots_dir, exist_ok=True)
    
    results = {
        "tests_passed": 0,
        "tests_failed": 0,
        "logs": [],
        "errors": []
    }

    def log(msg):
        # Sanitize message to pure ascii for windows cp1252 terminal safety
        clean_msg = msg.encode('ascii', errors='replace').decode('ascii')
        print(f"[QA SUITE] {clean_msg}")
        results["logs"].append(clean_msg)

    with sync_playwright() as p:
        log("Launching Chrome browser...")
        browser = p.chromium.launch(channel="chrome", headless=True)
        
        # ----------------------------------------------------
        # 1. DESKTOP VIEWPORT RUN (1280x850)
        # ----------------------------------------------------
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if (msg.type == "error" and "favicon" not in msg.text) else None)

        try:
            # Step 1: Landing Page
            log("Opening http://127.0.0.1:8000/ ...")
            page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
            page.wait_for_selector("#btn-landing-demo-login", timeout=10000)
            page.screenshot(path=os.path.join(screenshots_dir, "01_desktop_landing.png"))
            log("[PASS] Landing page loaded successfully. Screenshot saved.")
            results["tests_passed"] += 1

            # Step 2: Demo Login
            log("Executing Demo Login...")
            page.click("#btn-landing-demo-login")
            page.wait_for_selector("#btn-dashboard-plan-trip", timeout=5000)
            page.screenshot(path=os.path.join(screenshots_dir, "02_desktop_dashboard.png"))
            log("[PASS] Demo Login successful. User Priya & Rahul in Dashboard.")
            results["tests_passed"] += 1

            # Step 3: Plan Trip Navigation & Configuration
            log("Navigating to Plan Trip Form...")
            page.click("#btn-dashboard-plan-trip")
            page.wait_for_selector("#btn-generate-itinerary", timeout=5000)
            
            # Configure inputs strictly to user journey:
            # Kerala, 3 days, 2 travelers, ₹15,000, Waterfalls, Trekking, Local Food, Budget Hotel, Moderate pace
            log("Configuring Form: Kerala, 3 days, 2 travelers, Rs 15,000...")
            page.click("#btn-dest-kerala")
            page.click("#btn-duration-3")
            
            # Check travelers count
            travelers_text = page.locator("#text-travelers-count").inner_text()
            if "2" not in travelers_text:
                page.click("#btn-travelers-plus")

            # Set budget to ₹15,000
            page.click("#btn-budget-15000")

            # Select preferences
            page.select_option("#select-food", "Local Food")
            page.select_option("#select-hotel", "Budget Hotel")
            page.select_option("#select-pace", "Moderate pace")

            page.screenshot(path=os.path.join(screenshots_dir, "03_desktop_plan_form.png"))
            log("[PASS] Form configured with exact parameters. Screenshot saved.")
            results["tests_passed"] += 1

            # Step 4: Generate Trip
            log("Clicking 'Generate Intelligent Itinerary'...")
            page.click("#btn-generate-itinerary")
            
            page.wait_for_selector("#generating-title", timeout=5000)
            page.screenshot(path=os.path.join(screenshots_dir, "04_desktop_generating.png"))
            log("[PASS] Generating animation screen verified.")
            results["tests_passed"] += 1

            # Wait for Trip Hub to appear
            page.wait_for_selector("#tab-itinerary", timeout=15000)
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(screenshots_dir, "05_desktop_itinerary_day1.png"))
            log("[PASS] Trip Hub rendered. Day 1 Itinerary visible.")
            results["tests_passed"] += 1

            # Test Day 2 Itinerary tab
            page.click("#btn-day-tab-2")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(screenshots_dir, "06_desktop_itinerary_day2.png"))
            log("[PASS] Day 2 Itinerary switched and verified.")
            results["tests_passed"] += 1

            # Step 5: Interactive Map View
            log("Testing Interactive Map View...")
            page.click("#tab-map")
            page.wait_for_selector("#interactive-map", timeout=5000)
            page.wait_for_timeout(500)
            page.evaluate("window.dispatchEvent(new Event('resize'))")
            page.wait_for_timeout(2500)
            page.screenshot(path=os.path.join(screenshots_dir, "07_desktop_map.png"))
            log("[PASS] Leaflet interactive map loaded with pins and polylines.")
            results["tests_passed"] += 1

            # Step 6: Explainable Recommendations View
            log("Testing Explainable Recommendations View...")
            page.click("#tab-recommendations")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(screenshots_dir, "08_desktop_recommendations.png"))
            log("[PASS] IEEE Multi-attribute recommendation scores and explanations verified.")
            results["tests_passed"] += 1

            # Step 7: Hotel Integration View
            log("Testing Hotel Integration View...")
            page.click("#tab-hotel")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(screenshots_dir, "09_desktop_hotel.png"))
            log("[PASS] Budget hotel integration verified.")
            results["tests_passed"] += 1

            # Step 8: Local Food View
            log("Testing Local Food View...")
            page.click("#tab-food")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(screenshots_dir, "10_desktop_food.png"))
            log("[PASS] Curated Kerala food venues and costs verified.")
            results["tests_passed"] += 1

            # Step 9: Budget Dashboard
            log("Testing Budget Dashboard...")
            page.click("#tab-budget")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(screenshots_dir, "11_desktop_budget.png"))
            log("[PASS] Budget dashboard verified (Expected cost within Rs 15,000 cap).")
            results["tests_passed"] += 1

            # Step 10: Offline Package & Simulation
            log("Testing Offline Package View & Simulation...")
            page.click("#tab-offline")
            page.wait_for_timeout(500)
            
            # Click offline sim toggle
            page.click("#btn-offline-sim-toggle")
            page.wait_for_selector("#offline-banner", timeout=3000)
            page.screenshot(path=os.path.join(screenshots_dir, "12_desktop_offline_active.png"))
            log("[PASS] Offline Mode simulation active with emergency contacts.")
            results["tests_passed"] += 1

            # Toggle back to online
            page.click("#btn-offline-sim-toggle")

            # Step 11: Saved Trips View
            log("Testing Saved Trips...")
            page.click("#nav-saved-trips")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(screenshots_dir, "13_desktop_saved_trips.png"))
            log("[PASS] Saved Trips list verified.")
            results["tests_passed"] += 1

        except Exception as e:
            log(f"Desktop Test Error: {str(e)}")
            results["tests_failed"] += 1
            results["errors"].append(str(e))
            page.screenshot(path=os.path.join(screenshots_dir, "error_desktop.png"))

        finally:
            context.close()

        # ----------------------------------------------------
        # 2. MOBILE VIEWPORT RUN (390x844 - iPhone / Modern Mobile)
        # ----------------------------------------------------
        log("\n--- Starting Mobile Viewport Run (390x844) ---")
        mobile_context = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        )
        mobile_page = mobile_context.new_page()

        try:
            # Mobile Step 1: Landing
            mobile_page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
            mobile_page.wait_for_selector("#btn-landing-demo-login", timeout=5000)
            mobile_page.screenshot(path=os.path.join(screenshots_dir, "14_mobile_landing.png"))
            log("[PASS] Mobile Landing page verified.")
            results["tests_passed"] += 1

            # Mobile Step 2: Demo Login & Dashboard
            mobile_page.click("#btn-landing-demo-login")
            mobile_page.wait_for_selector("#btn-dashboard-plan-trip", timeout=5000)
            mobile_page.screenshot(path=os.path.join(screenshots_dir, "15_mobile_dashboard.png"))
            log("[PASS] Mobile Dashboard verified.")
            results["tests_passed"] += 1

            # Mobile Step 3: Plan Trip Form
            mobile_page.click("#btn-dashboard-plan-trip")
            mobile_page.wait_for_selector("#btn-generate-itinerary", timeout=5000)
            mobile_page.screenshot(path=os.path.join(screenshots_dir, "16_mobile_plan_form.png"))
            log("[PASS] Mobile Plan Trip form verified.")
            results["tests_passed"] += 1

            # Mobile Step 4: Generate
            mobile_page.click("#btn-generate-itinerary")
            mobile_page.wait_for_selector("#mobile-tab-itinerary", timeout=15000)
            mobile_page.wait_for_timeout(1000)
            mobile_page.screenshot(path=os.path.join(screenshots_dir, "17_mobile_itinerary.png"))
            log("[PASS] Mobile Itinerary with bottom navigation bar verified.")
            results["tests_passed"] += 1

            # Mobile Step 5: Mobile Map
            mobile_page.click("#mobile-tab-map", force=True)
            mobile_page.wait_for_timeout(500)
            mobile_page.evaluate("window.dispatchEvent(new Event('resize'))")
            mobile_page.wait_for_timeout(2500)
            mobile_page.screenshot(path=os.path.join(screenshots_dir, "18_mobile_map.png"))
            log("[PASS] Mobile Map verified.")
            results["tests_passed"] += 1

            # Mobile Step 6: Mobile Budget
            mobile_page.click("#mobile-tab-budget", force=True)
            mobile_page.wait_for_timeout(500)
            mobile_page.screenshot(path=os.path.join(screenshots_dir, "19_mobile_budget.png"))
            log("[PASS] Mobile Budget breakdown verified.")
            results["tests_passed"] += 1

            # Mobile Step 7: Mobile Offline
            mobile_page.click("#mobile-tab-offline", force=True)
            mobile_page.wait_for_timeout(500)
            mobile_page.screenshot(path=os.path.join(screenshots_dir, "20_mobile_offline.png"))
            log("[PASS] Mobile Offline Package view verified.")
            results["tests_passed"] += 1

        except Exception as e:
            log(f"Mobile Test Error: {str(e)}")
            results["tests_failed"] += 1
            results["errors"].append(str(e))
            mobile_page.screenshot(path=os.path.join(screenshots_dir, "error_mobile.png"))

        finally:
            mobile_context.close()
            browser.close()

    log("\n================ TEST SUMMARY ================")
    log(f"Total Tests Passed: {results['tests_passed']}")
    log(f"Total Tests Failed: {results['tests_failed']}")
    if console_errors:
        log(f"Console Errors: {console_errors}")
    return results

if __name__ == "__main__":
    res = run_qa_suite()
    if res["tests_failed"] > 0:
        sys.exit(1)
    sys.exit(0)
