from flask import Flask, request, jsonify
import numpy as np
from model_loader import load_model, load_scaler
import logging




app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained model and scaler
model = load_model('best_model.pickle')
scaler = load_scaler('scaler.pickle')

@app.route('/predict', methods=['POST'])
def predict():
    
    # Extract values from the request JSON
    request_data = request.json
    # //print(request_data)
    
    # Extract feature values from the request data
    feature_names = ['worst perimeter', 'worst concave points', 'mean concave points', 'mean concavity', 'worst radius']
    data = [request_data.get(feature) for feature in feature_names]

    # Ensure the correct number of features
    if len(data) != 5:
        return jsonify({"error": "Expected 5 input values"}), 400

    # Transform input data using the same scaler used during training
    final_input = scaler.transform([data])

    # Make prediction
    output = int(model.predict(final_input)[0])

    # Return prediction result as JSON
    logging.info("Prediction Successfull")
    if output == 0:
        return jsonify({"prediction_text": "The Cancer is Benign as the output is {}!".format(output)})
    else:
        return jsonify({"prediction_text": "The Cancer is Malignant as the output is {}!".format(output)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

