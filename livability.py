import requests

def get_current_temperature(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
    try:
        resp = requests.get(url, timeout=5).json()
        return resp.get('current', {}).get('temperature_2m', 30.0) # default 30C
    except Exception:
        return 30.0

def compute(df):
    mean_lat = df["lat"].mean()
    mean_lon = df["lon"].mean()
    current_temp = get_current_temperature(mean_lat, mean_lon)

    # Offset risk based on real-time ambient heat
    temp_factor = (current_temp - 30.0) * 1.5

    df["risk"] = df["prediction"] + temp_factor
    df["risk"] = df["risk"].clip(0, 100)

    df["livability"] = (
        (100-df["risk"])*0.4 +
        df["NDVI"]*100*0.3 -
        df["NDBI"]*100*0.2 -
        df["NightLights"]*0.1
    )

    df["ambient_temp_celsius"] = current_temp

    return df
