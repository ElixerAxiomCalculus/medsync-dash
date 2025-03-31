#For starting a Flask server
from flask import Flask, jsonify, render_template, request
import pandas as pd
import joblib


app = Flask(__name__)

# Test endpoint
@app.route('/')
def home():
    return jsonify({'message': 'MedSync API is running'})

# Prediction endpoint (initially empty)
@app.route('/predict_single', methods=['POST'])
def predict_single():
    data = request.get_json()
    X = [[data['stock'], data['expiry']]]
    model = joblib.load('models/model.pkl')
    prediction = model.predict(X)[0]
    return jsonify({'prediction': float(prediction)})

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    data = request.get_json()
    model = joblib.load('models/model.pkl')
    X = list(zip(data['current_stock'], data['expiry']))
    predictions = model.predict(X)
    return jsonify({'predictions': [float(p) for p in predictions]})


@app.route('/predict', methods=['GET'])
def predict_default():
    model = joblib.load('models/model.pkl')
    data = pd.read_csv('data/data.csv')
    X = data[['Current_Stock', 'Days_Until_Expiry']]
    predictions = model.predict(X)
    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
