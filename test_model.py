import joblib
import pandas as pd


model = joblib.load("ddos_model.pkl")


sample = {
   "response_time_ms": 250,
    "endpoint": "/form",
    "hour": 14,
    "ip_class": "B",
    "user_agent_type": "Browser"
}



df = pd.DataFrame([sample])


df = pd.get_dummies(df)


model_features = model.feature_names_in_
for col in model_features:
    if col not in df.columns:
        df[col] = 0

df = df[model_features]

prediction = model.predict(df)
print(" Tahmin:", prediction[0])
