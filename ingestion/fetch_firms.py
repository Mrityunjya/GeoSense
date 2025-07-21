import pandas as pd

def fetch_firms_from_csv(filepath="data/MODIS_C6_Global_24h.csv"):
    df = pd.read_csv(filepath)
    
    # Filter high confidence fire alerts
    high_conf = df[df['confidence'] == 'high']  # Adjust based on your file format
    
    alerts = []
    for _, row in high_conf.iterrows():
        alert = {
            "location": f"{row['latitude']}, {row['longitude']}",
            "text": "Fire alert from FIRMS",
            "coordinates": (row['latitude'], row['longitude']),
            "timestamp": row['acq_date']
        }
        alerts.append(alert)
    
    return alerts
