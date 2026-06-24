import pandas as pd

def get_top_drivers(importance, features):
    drivers = pd.Series(importance, index=features).sort_values(ascending=False).head(3)
    return drivers.index.tolist()

def green_deficit(ndvi):
    ideal = 0.6
    return round(ideal - ndvi, 2)

def cooling_potential(deficit):
    return round(deficit * 4, 2)

def people_at_risk(ndbi):
    # NDBI ranges from -1 to 1. Higher value = highly built up/dense.
    # We map NDBI to a base population density between 2,000 and 45,000 per grid point
    # Scale: NDBI + 1 is 0 to 2.
    base_pop = 2000 + ((ndbi + 1) / 2) * 43000
    # People at severe heat risk (approx 35% vulnerable demograhic)
    return int(base_pop * 0.35)

def future_risk(risk_score):
    return round(risk_score * 1.05, 2)

def early_warning(fut_risk):
    return bool(fut_risk > 80)

def mitigation(drivers, risk):
    actions = []
    
    if any(x in drivers for x in ["NDVI", "EVI", "SAVI"]):
        actions.extend([
            "Increase roadside tree plantation",
            "Create pocket parks and green buffers",
            "Vertical gardening on buildings"
        ])
        
    if any(x in drivers for x in ["NDBI", "LandCover", "Albedo"]):
        actions.extend([
            "Adopt cool roof technology",
            "Use reflective pavement materials",
            "Limit new concrete development"
        ])
        
    if "Population" in drivers:
        actions.extend([
            "Establish temporary cooling shelters",
            "Install drinking water kiosks",
            "Reschedule outdoor labor hours"
        ])
        
    if "LST" in drivers or "LST_Celsius" in drivers or "NightLights" in drivers:
        actions.extend([
            "Build shaded pedestrian corridors",
            "Deploy misting stations in markets",
            "Increase urban water bodies"
        ])
        
    if risk > 70:
        actions.extend([
            "Issue heat-wave alert to citizens",
            "Activate emergency heat response teams"
        ])
        
    return list(set(actions))

def resilience(risk_score):
    return round(100 - risk_score, 2)

def livability_status(risk, res, green_def):
    if risk < 40 and res > 60 and green_def < 0.2:
        return "Highly Livable"
    elif risk < 60 and res > 45:
        return "Moderately Livable"
    elif risk < 75:
        return "Heat-Stressed"
    else:
        return "Critical - Immediate Intervention Needed"

def urban_health_summary(status):
    if status == "Highly Livable":
        return "This locality currently maintains a healthy balance between built environment and natural cooling."
    elif status == "Moderately Livable":
        return "Thermal comfort is acceptable but vegetation loss and urban density are beginning to affect living conditions."
    elif status == "Heat-Stressed":
        return "This area is experiencing significant urban heat stress due to reduced greenery and increased surface temperature."
    else:
        return "Severe environmental stress detected. Immediate mitigation measures are strongly recommended."

def enrich_dataframe(df, model, features):
    if hasattr(model, 'feature_importances_'):
        top_drivers = get_top_drivers(model.feature_importances_, features)
    else:
        top_drivers = ["NDVI", "NDBI", "LST"]

    df["green_deficit"] = df["NDVI"].apply(green_deficit)
    df["cooling_potential"] = df["green_deficit"].apply(cooling_potential)
    
    # Calculate population dynamically using NDBI (Normalized Difference Built-up Index)
    df["people_at_risk"] = df.apply(lambda row: people_at_risk(row["NDBI"]), axis=1) 
    
    df["future_risk_3months"] = df["risk"].apply(future_risk)
    df["early_warning"] = df["future_risk_3months"].apply(early_warning)
    df["resilience_score"] = df["risk"].apply(resilience)
    

    df["top_drivers"] = [top_drivers for _ in range(len(df))]
    df["mitigation_actions"] = df.apply(lambda row: mitigation(top_drivers, row["risk"]), axis=1)
    
    df["livability_status"] = df.apply(lambda row: livability_status(row["risk"], row["resilience_score"], row["green_deficit"]), axis=1)
    df["health_summary"] = df["livability_status"].apply(urban_health_summary)
    
    df["livability_index"] = (
        (100 - df["risk"]) * 0.5 + 
        df["resilience_score"] * 0.3 + 
        (1 - df["green_deficit"]) * 100 * 0.2
    )
    
    return df
