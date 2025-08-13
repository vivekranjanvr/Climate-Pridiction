from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
from models.climate_model import ClimateModel
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize climate model
climate_model = ClimateModel()

# In-memory storage for history
history_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Get prediction from model
        prediction = climate_model.predict(data)
        
        # Save to history
        history_data.append({
            'id': len(history_data) + 1,
            'temperature': data.get('temperature', 25),
            'humidity': data.get('humidity', 60),
            'co2_levels': data.get('co2_levels', 400),
            'precipitation': data.get('precipitation', 100),
            'impact_score': prediction,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        return jsonify({
            'prediction': prediction,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    try:
        return jsonify(climate_model.get_analysis())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        return jsonify(history_data[-100:])  # Return last 100 records
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        global history_data
        history_data = [record for record in history_data if record['id'] != record_id]
        return jsonify({'message': 'Record deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
