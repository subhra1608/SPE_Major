import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from model_loader import load_model, load_scaler
from elasticSearch_log import push_logs_to_elasticsearch
import datetime

app = Flask(__name__)

# Load the trained model and scaler
model = load_model('best_model.pickle')
scaler = load_scaler('scaler.pickle')

# Configure logging to use the existing log file 'logging.log'
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('logging.log', maxBytes=10240, backupCount=10)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract values from the request JSON
        request_data = request.json
        app.logger.info("Welcome to breast cancer prediction!")
        
        # Extract feature values from the request data
        feature_names = ['worst perimeter', 'worst concave points', 'mean concave points', 'mean concavity', 'worst radius']
        data = [request_data.get(feature) for feature in feature_names]

        # Ensure the correct number of features
        if len(data) != 5:
            return jsonify({"error": "Expected 5 input values"}), 400
            app.logger.info("Prediction cannot be processed due to inappropriate input")

        # Transform input data using the same scaler used during training
        final_input = scaler.transform([data])

        # Make prediction
        output = int(model.predict(final_input)[0])

        # Log prediction result to both file and Elasticsearch
        app.logger.info("Prediction Successfull!")
        prediction_text = "The Cancer is Benign" if output == 0 else "The Cancer is Malignant"
        app.logger.info(prediction_text)
        # es.index(index="predictions", body={"prediction_text": prediction_text})
        push_logs_to_elasticsearch()

        # Return prediction result as JSON
        return jsonify({"prediction_text": prediction_text}), 200
    
    except Exception as e:
        app.logger.error(f"Error occurred during prediction: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
