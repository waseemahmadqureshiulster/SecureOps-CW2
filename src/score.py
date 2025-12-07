import os
import json
import joblib
import pandas as pd
import logging

def init():
    global model
    # Get the base path
    base_path = os.getenv("AZUREML_MODEL_DIR")
    logging.info(f"Base path: {base_path}")
    
    # SEARCH for the model.pkl file instead of guessing
    model_path = ""
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == "model.pkl":
                model_path = os.path.join(root, file)
                break
    
    if not model_path:
        raise Exception(f"Could not find model.pkl in {base_path}")

    logging.info(f"Loading model from: {model_path}")
    model = joblib.load(model_path)

def run(raw_data):
    try:
        data = json.loads(raw_data)
        input_df = pd.DataFrame(data['data'])
        result = model.predict(input_df)
        return result.tolist()
    except Exception as e:
        return {"error": str(e)}