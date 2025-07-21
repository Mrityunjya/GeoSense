@echo off
title 🌍 Launching GeoSense AI System...

:: Optional: Activate virtual environment if used
:: call venv\Scripts\activate

:: Start backend API in new terminal
start cmd /k "cd backend && uvicorn main:app --reload"

:: Delay for backend to boot up
timeout /t 3 >nul

:: Start frontend dashboard
start cmd /k "cd frontend\dashboard && python -m streamlit run app.py"

:: Optional: Open in browser (after short delay)
timeout /t 5 >nul
start http://localhost:8501

echo All systems are launching 🚀
pause
