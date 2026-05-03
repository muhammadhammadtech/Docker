from flask import Flask, request, jsonify
import psycopg2
import os
from app import HousePricePredictor

app = Flask(__name__)

predictor = HousePricePredictor()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'mldata'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/', methods=['GET'])
def api_documentation():
    docs = {
        'title': 'House Price Prediction API',
        'version': '1.0',
        'endpoints': {
            'GET /': 'API documentation',
            'GET /health': 'Health check',
            'POST /predict': 'Predict house price (requires: size, bedrooms, age)',
            'GET /predictions': 'Get recent predictions from database',
            'POST /train': 'Retrain the model'
        },
        'example_request': {
            'url': '/predict',
            'method': 'POST',
            'body': {
                'size': 2500,
                'bedrooms': 3,
                'age': 10
            }
        }
    }
    return jsonify(docs)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor.is_trained
    })

@app.route('/predict', methods=['POST'])
def predict_price():
    try:
        data = request.get_json()
        required_fields = ['size', 'bedrooms', 'age']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        prediction = predictor.predict(
            data['size'], 
            data['bedrooms'], 
            data['age']
        )
        store_prediction(data, prediction)
        return jsonify({
            'prediction': round(prediction, 2),
            'input': data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predictions', methods=['GET'])
def get_predictions():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, size, bedrooms, age, predicted_price, created_at 
            FROM predictions 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        results = cursor.fetchall()
        predictions = []
        for row in results:
            predictions.append({
                'id': row[0],
                'size': row[1],
                'bedrooms': row[2],
                'age': row[3],
                'predicted_price': float(row[4]),
                'created_at': row[5].isoformat()
            })
        cursor.close()
        conn.close()
        return jsonify({'predictions': predictions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def store_prediction(input_data, prediction):
    try:
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (size, bedrooms, age, predicted_price)
            VALUES (%s, %s, %s, %s)
        """, (input_data['size'], input_data['bedrooms'], input_data['age'], prediction))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error storing prediction: {e}")

@app.route('/train', methods=['POST'])
def retrain_model():
    try:
        predictor.train_model()
        return jsonify({'message': 'Model retrained successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    predictor.load_model()
    app.run(host='0.0.0.0', port=5000, debug=False)
