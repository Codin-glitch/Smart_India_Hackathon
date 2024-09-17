from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

model = joblib.load("random_forest_outlier_classifier.joblib")
scaler = joblib.load("scaler (1).joblib")

d = np.array([(-0.184, 0.984,-0.068)])
value = scaler.transform(d)
prediction = model.predict(value)

print(prediction)

