import requests
import concurrent.futures

GOOGLE_API_KEY = "AIzaSyDLJ41jOwhZCitWvqc7ot8UAPsvGVTxq4o"
loc_cache = {}

def get_suburb(lat, lon):
    rounded = (round(lat, 3), round(lon, 3))
    if rounded in loc_cache:
        return loc_cache[rounded]

    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_API_KEY}"
    try:
        resp = requests.get(url, timeout=5).json()
        if resp['status'] == 'OK':
            for result in resp['results']:
                for comp in result['address_components']:
                    if 'sublocality' in comp['types'] or 'locality' in comp['types'] or 'neighborhood' in comp['types']:
                        name = comp['long_name']
                        loc_cache[rounded] = name
                        return name
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    loc_cache[rounded] = "Unknown"
    return "Unknown"

def add_locality(df):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for _, r in df.iterrows():
            futures.append(executor.submit(get_suburb, r.lat, r.lon))
        names = [f.result() for f in futures]

    df["locality"] = names
    return df

if __name__=="__main__":
    import pandas as pd
    df = pd.DataFrame({
        "lat":[19.076],
        "lon":[72.877]
    })
    print(add_locality(df))