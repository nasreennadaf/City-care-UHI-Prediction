import folium
from folium.plugins import HeatMap
from branca.element import Template, MacroElement

def generate_current_heatmap(df, city):
    """
    Generate a Folium HTML heatmap for the current risk.
    """
    if df.empty:
        return "<p>No data available for heatmap</p>"
        
    # Center map on the average coordinates
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB dark_matter")
    
    # Extract coordinates and weights (risk score)
    heat_data = [[row['lat'], row['lon'], row['risk']] for index, row in df.iterrows()]
    
    # Add HeatMap layer
    HeatMap(
        heat_data,
        radius=35,
        blur=25,
        max_zoom=13,
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
    ).add_to(m)
    
    # --- Add Legend ---
    template = """
    {% macro html(this, kwargs) %}
    <div style="position: fixed; 
         bottom: 50px; left: 50px; width: 180px; height: 160px; 
         background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
         ">&nbsp;<b>Current Heat Risk</b><br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:blue"></i>&nbsp;Safe / Cool<br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:lime"></i>&nbsp;Mild<br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:yellow"></i>&nbsp;Moderate<br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:orange"></i>&nbsp;High Risk<br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:red"></i>&nbsp;Severe Danger<br>
    </div>
    {% endmacro %}
    """
    macro = MacroElement()
    macro._template = Template(template)
    m.get_root().add_child(macro)

    # Return HTML representation
    return m._repr_html_()


def generate_future_heatmap(df, city):
    """
    Generate a Folium HTML heatmap for the 3-month future risk projection.
    """
    if df.empty:
        return "<p>No data available for heatmap</p>"
        
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB positron")
    
    # Extract coordinates and weights (future_risk_3months score)
    heat_data = [[row['lat'], row['lon'], row['future_risk_3months']] for index, row in df.iterrows()]
    
    HeatMap(
        heat_data,
        radius=35,
        blur=25,
        max_zoom=13,
        gradient={0.2: 'teal', 0.5: 'yellow', 0.7: 'orange', 1.0: 'darkred'}
    ).add_to(m)
    
    # --- Add Legend ---
    template = """
    {% macro html(this, kwargs) %}
    <div style="position: fixed; 
         bottom: 50px; left: 50px; width: 220px; height: 140px; 
         background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
         ">&nbsp;<b>Projected 3-Month Risk</b><br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:teal"></i>&nbsp;Stable<br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:yellow"></i>&nbsp;Emerging Threat<br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:orange"></i>&nbsp;High Projected Risk<br>
         &nbsp;<i class="fa fa-circle fa-1x" style="color:darkred"></i>&nbsp;Critical Projection<br>
    </div>
    {% endmacro %}
    """
    macro = MacroElement()
    macro._template = Template(template)
    m.get_root().add_child(macro)
    
    return m._repr_html_()
