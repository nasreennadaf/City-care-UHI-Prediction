from gee_engine import extract
from xgboost import XGBRegressor
import joblib

df = extract("Mumbai")

features = [
"NDVI","NDBI","EVI","SAVI","Albedo",
"MNDWI","IBI","Elevation","Slope","NightLights"
]

X = df[features]
y = df["LST"]

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05
)

model.fit(X,y)

joblib.dump(model,"uhi_model.pkl")

print("MODEL SAVED")