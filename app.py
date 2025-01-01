import requests
import os

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/verify-recaptcha', methods=['POST'])
def verify_recaptcha():
    user_response = request.json
    res = requests.post('https://www.google.com/recaptcha/api/siteverify', json={
        'secret': os.environ.get('RECAPTCHA_SECRET'),
        'response': user_response['recaptchaResponse']
    })
    
    return res.content
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
