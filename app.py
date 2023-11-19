from flask import Flask, render_template, request, jsonify
from jsonschema import validate, ValidationError
from pymongo import MongoClient
from datetime import datetime, timedelta
from celery import Celery
import os

app = Flask(__name__)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
app.config['DB_NAME'] = os.environ.get('DB_NAME', 'dev')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)

# Initialize Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Create MongoDB connection
client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['DB_NAME']]

LOG_SCHEMA = {
    "type": "object",
    "required": ["level", "message", "timestamp"],
    "properties": {
        "level": {"type": "string"},
        "message": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"}
    }
}

@celery.task
def process_log(log_data):
    # Validate input against the schema
    validate(log_data, LOG_SCHEMA)

    # Insert into MongoDB
    db.logs.insert_one(log_data)
    return {"status": "success"}

@app.route('/')
def index():
    return render_template('index.html', stylesheet='styles.css')

@app.route('/search', methods=['POST'])
def search_logs():
    try:
        query_params = {key: request.form.get(key) for key in request.form}
        filtered_logs = filter_logs(query_params)
        return render_template('result.html', logs=filtered_logs)
    except Exception as e:
        return render_template('error.html', error=str(e))

def filter_logs(query_params):
    query = {}
    for key, value in query_params.items():
        if key == 'message':
            query[key] = {'$regex': f'.*{value}.*', '$options': 'i'}
        elif key == 'timestamp':
            start_date = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            end_date = start_date + timedelta(days=1)
            query[key] = {'$gte': start_date, '$lt': end_date}
        elif value:
            query[key] = value
    return list(db.logs.find(query))

@app.route('/ingest', methods=['POST'])
def ingest_logs():
    try:
        log_data = request.get_json()

        # Use Celery for async processing
        process_log.delay(log_data)

        return jsonify({"status": "accepted"})
    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=app.config['DEBUG'])
