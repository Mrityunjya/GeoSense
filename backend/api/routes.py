from fastapi import APIRouter
from datetime import datetime
import pandas as pd

router = APIRouter()

# Simulated in-memory data (replace with real ingestion)
FAKE_DATA = [
    {"lat": 37.7749, "lon": -122.4194, "text": "Wildfire spreading in California", "severity": "high", "source": "Twitter", "timestamp": datetime.utcnow()},
    {"lat": 19.0760, "lon": 72.8777, "text": "Heavy rains in Mumbai", "severity": "medium", "source": "NASA", "timestamp": datetime.utcnow()}
]

@router.get("/map")
def get_events():
    return [dict(item, timestamp=item["timestamp"].isoformat()) for item in FAKE_DATA]

@router.get("/")
def root():
    return {"status": "GeoSense API is running"}
