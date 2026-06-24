import requests
import json

def fetch_and_print_pune_report():
    report_lines = []
    
    def log(msg=""):
        print(msg)
        report_lines.append(msg)

    log("================ SMART HEAT RISK REPORT ================")
    log("Fetching live satellite and weather data... (This takes about ~25 seconds)")
    
    try:
        resp = requests.get("http://127.0.0.1:5000/analyze?city=Pune")
        if resp.status_code != 200:
            log(f"Error fetching data: {resp.status_code}")
            return
            
        data = resp.json()
        
        raw_localities = [f["properties"].get("locality", "Unknown") for f in data["features"]]
        # Filter out "Unknown", empty strings, or strings that are just whitespace
        valid_localities = [loc.strip() for loc in raw_localities if loc and loc.strip() and loc.strip() != "Unknown"]
        localities = list(set(valid_localities))
        
        log("\n=========== AVAILABLE LOCALITIES ===========")
        for i, loc in enumerate(sorted(localities), start=1):
            log(f"{i}. {loc}")
            
        log("\n🏆 TOP 10 MOST LIVABLE LOCALITIES IN PUNE:")
        for idx, loc in enumerate(data.get("rankings", {}).get("most_livable", [])[:10], start=1):
            log(f"  {idx}. {loc['locality']} (Livability Index: {loc['livability_index']:.2f})")
            
        log("\n🚨 TOP 10 LEAST LIVABLE LOCALITIES IN PUNE:")
        for idx, loc in enumerate(data.get("rankings", {}).get("least_livable", [])[:10], start=1):
            log(f"  {idx}. {loc['locality']} (Livability Index: {loc['livability_index']:.2f})")
            
        
        sample_feature = next((f for f in data["features"] if f["properties"].get("locality", "Unknown") != "Unknown"), None)
        
        if sample_feature:
            sample = sample_feature["properties"]
            coords = sample_feature["geometry"]["coordinates"]
            log(f"\n================ SMART HEAT RISK REPORT ================\n")
            log(f"📍 Locality: {sample['locality']}\n")

            log(f"🔥 Heat Risk Score: {sample['risk']:.2f}")
            log(f"   Optimal: < 30 | Moderate: 30 – 60 | High: > 60\n")

            log(f"🧠 Main Heat Drivers:")
            for d in sample.get("top_drivers", []):
                log("   • " + d)

            log(f"\n🌱 Green Deficit: {sample['green_deficit']} %")
            log(f"   Optimal: < 20 | Concerning: 20 – 40 | Critical: > 40\n")

            log(f"❄ Cooling Potential: {sample['cooling_potential']} %")
            log(f"   Optimal: > 60 | Concerning: 30 – 60 | Critical: < 30\n")

            log(f"👥 People at Risk: {sample.get('people_at_risk', 'Unknown')} persons")
            log(f"   Optimal: < 500 | Concerning: 500 – 2000 | Critical: > 2000\n")

            log(f"⏳ Future Risk (3 months): {sample['future_risk_3months']}")
            log(f"   Optimal: < 40 | Concerning: 40 – 70 | Critical: > 70\n")
            
            if sample.get('early_warning'):
                log(f"🚨 EARLY WARNING: High Risk Trend Detected!\n")

            log(f"🛡 Urban Resilience Score: {sample['resilience_score']:.2f}\n")

            log("🛠 AI-Recommended Mitigation Actions:\n")
            for s in sample.get("mitigation_actions", []):
                log("   • " + s)

            log("\n=======================================================\n")
            
    except Exception as e:
        log(f"Failed to connect to backend: {e}")
        
    # Write everything to file
    with open("pune_realtime_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")
        
    print("\n✅ Report saved to pune_realtime_report.txt!")

if __name__ == "__main__":
    fetch_and_print_pune_report()
