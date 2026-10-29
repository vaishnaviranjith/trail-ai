@echo off
echo ========================================================
echo Starting Trail AI - Smart Trip Planner MVP
echo Grounded in IEEE Research (DOI: 10.1109/ICUIS67429.2025.11380545)
echo ========================================================
cd /d "%~dp0"
if exist "trail ai\backend\main.py" (
    cd "trail ai\backend"
    python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
) else if exist "backend\main.py" (
    cd backend
    python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
) else (
    echo Error: Could not locate backend/main.py.
    pause
)
