import os
import json
import joblib
import pandas as pd
import logging

def init():
    global model
    try:
        # Get the base path
        base_path = os.getenv("AZUREML_MODEL_DIR")
        logging.info(f"Base path: {base_path}")
        
        # SEARCH for the model.pkl file
        model_path = None
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file == "model.pkl":
                    model_path = os.path.join(root, file)
                    break
            if model_path:
                break
        
        if not model_path:
            raise Exception(f"Could not find model.pkl in {base_path}")

        logging.info(f"Loading model from: {model_path}")
        model = joblib.load(model_path)
        logging.info("Model loaded successfully")
        
    except Exception as e:
        logging.error(f"Error in init(): {str(e)}")
        raise

def run(raw_data):
    try:
        logging.info(f"Received request: {raw_data}")
        data = json.loads(raw_data)
        input_df = pd.DataFrame(data['data'])
        result = model.predict(input_df)
        logging.info(f"Prediction: {result.tolist()}")
        return result.tolist()
    except Exception as e:
        error_msg = {"error": str(e)}
        logging.error(f"Error in run(): {error_msg}")
        return error_msg