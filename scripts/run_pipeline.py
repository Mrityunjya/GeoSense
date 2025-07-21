from ai.model import DisasterClassifier
from ingestion.fetch_firms import get_firms_alerts
from ingestion.fetch_usgs_weather import get_usgs_alerts
from backend.notifier import send_sms_alert
import time

model = DisasterClassifier()

def pipeline():
    print("🔁 Running GeoSense AI Pipeline...")

    # Get data from external sources
    firms_alerts = get_firms_alerts()
    usgs_alerts = get_usgs_alerts()

    combined = firms_alerts + usgs_alerts
    for alert in combined:
        text = alert['text']
        label, confidence = model.predict(text)

        print(f"[{label}] {text} (confidence: {confidence:.2f})")

        if label == "POSITIVE" and confidence > 0.85:
            send_sms_alert(f"🚨 Alert: {text[:100]}")
            print("✅ Alert sent")

if __name__ == "__main__":
    while True:
        pipeline()
        time.sleep(300)  # 5 min interval
