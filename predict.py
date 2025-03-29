import sys
import json
import joblib
import pandas as pd  


print("Received arguments:", sys.argv, file=sys.stderr)


if len(sys.argv) < 4:
    print(json.dumps({"error": "Missing input arguments"}))
    sys.exit(1)


try:
    packet_size = float(sys.argv[1])
    request_frequency = float(sys.argv[2])
    port = int(sys.argv[3])
except ValueError:
    print(json.dumps({"error": "Invalid input data format"}))
    sys.exit(1)


try:
    model = joblib.load("random_forest_model.pkl")  
    scaler = joblib.load("scaler.pkl")  
except Exception as e:
    print(json.dumps({"error": f"Model or Scaler loading failed: {str(e)}"}))
    sys.exit(1)


features = pd.DataFrame([[packet_size, request_frequency, port]], columns=["packet_size", "request_frequency", "port"])


features_scaled = scaler.transform(features)


prediction = model.predict(features_scaled)


prediction_value = int(prediction[0]) if isinstance(prediction[0], (int, float)) else str(prediction[0])


print(json.dumps({"prediction": prediction_value}))


