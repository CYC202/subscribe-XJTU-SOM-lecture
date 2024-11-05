from flask import Flask, request, jsonify
from lecture_monitor import LectureMonitor
import os
import re
import time
from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)

URL = "https://som.xjtu.edu.cn/xsdt/xshd.htm"
current_directory = os.path.dirname(os.path.abspath(__file__))
EMAIL_CREDENTIALS_FILE = os.path.join(current_directory, "email_credentials.txt")
TO_EMAILS_FILE = os.path.join(current_directory, "to_emails.txt")
STORAGE_FILE = os.path.join(current_directory, "sent_lectures.txt")

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

@app.route('/subscribe', methods=['GET', 'POST'])
@app.route('/subscribe/<email>', methods=['GET'])
def subscribe(email=None):
    monitor = LectureMonitor(URL, EMAIL_CREDENTIALS_FILE, TO_EMAILS_FILE, STORAGE_FILE)

    if request.method == 'POST':
        email = request.json.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        message = monitor.subscribe(email)
        return jsonify({'message': message})

    elif email:
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        message = monitor.subscribe(email)
        return jsonify({'message': message})

    else:
        return jsonify({'error': 'Invalid email format'}), 400

@app.route('/unsubscribe', methods=['GET', 'POST'])
@app.route('/unsubscribe/<email>', methods=['GET'])
def unsubscribe(email=None):
    monitor = LectureMonitor(URL, EMAIL_CREDENTIALS_FILE, TO_EMAILS_FILE, STORAGE_FILE)

    if request.method == 'POST':
        email = request.json.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        message = monitor.unsubscribe(email)
        return jsonify({'message': message})

    elif email:
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        message = monitor.unsubscribe(email)
        return jsonify({'message': message})

    else:
        return jsonify({'error': 'Invalid email format'}), 400

@app.route('/monitor', methods=['GET'])
def run_monitor():
    monitor = LectureMonitor(URL, EMAIL_CREDENTIALS_FILE, TO_EMAILS_FILE, STORAGE_FILE)
    monitor.monitor()
    return jsonify({'message': 'Monitor task executed successfully'})

@app.route('/subscribed_emails/<password>', methods=['GET'])
def get_subscribed_emails(password):
    psd = os.getenv('PASSWORD')
    print(psd, password)
    if password == psd:
        monitor = LectureMonitor(URL, EMAIL_CREDENTIALS_FILE, TO_EMAILS_FILE, STORAGE_FILE)
        subscribed_emails = list(monitor.to_emails)
        return jsonify({'subscribed_emails': subscribed_emails})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008)
    while True:
        run_monitor()  # Call the monitor function
        time.sleep(3600)  # Sleep for 1 hour (3600 seconds)
