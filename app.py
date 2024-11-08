from flask import Flask, request, jsonify
from lecture_monitor import LectureMonitor
import os
import re
from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)

load_dotenv(find_dotenv('.env'))
 
# Configuration Variables
URL = os.getenv('URL')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lecture_monitor.db")

# Initialize LectureMonitor instance and start monitoring thread
monitor = LectureMonitor(URL, EMAIL_ADDRESS, EMAIL_PASSWORD, DB_FILE)
monitor.start_monitoring()

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

@app.route('/subscribe', methods=['GET', 'POST'])
@app.route('/subscribe/<email>', methods=['GET'])
def subscribe(email=None):
    if request.method == 'POST':
        email = request.json.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
    elif email:
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
    else:
        return jsonify({'error': 'Email is required'}), 400

    message = monitor.subscribe(email)
    return jsonify({'message': message})

@app.route('/unsubscribe', methods=['GET', 'POST'])
@app.route('/unsubscribe/<email>', methods=['GET'])
def unsubscribe(email=None):
    if request.method == 'POST':
        email = request.json.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
    elif email:
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
    else:
        return jsonify({'error': 'Email is required'}), 400

    message = monitor.unsubscribe(email)
    return jsonify({'message': message})

@app.route('/monitor', methods=['GET'])
def run_monitor():
    monitor.monitor()
    return jsonify({'message': 'Monitor task executed successfully'})

@app.route('/subscribed_emails/<password>', methods=['GET'])
def get_subscribed_emails(password):
    if password == os.getenv('PASSWORD'):

        subscribed_emails = monitor.get_subscribers()
        return jsonify({'subscribed_emails': subscribed_emails})
    else:
        return jsonify({'error': 'Unauthorized'}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008)
    while True:
        monitor.monitor()