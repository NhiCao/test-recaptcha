import requests
import os

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/verify-recaptcha', methods=['POST'])
def verify_recaptcha():
    recaptcha_response = request.form.get('g-recaptcha-response')

    if not recaptcha_response:
        return jsonify({'success': False, 'message': 'Missing reCAPTCHA response.'}), 400

    secret_key = os.getenv('RECAPTCHA_SECRET')
    if not secret_key:
        return jsonify({'success': False, 'message': 'Secret key is not configured.'}), 500

    google_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    response = requests.post(google_verify_url, data=payload)
    verification = response.json()

    if verification.get('success'):
        return jsonify({'success': True, 'message': 'Verification successful.'})
    else:
        return jsonify({
            'success': False,
            'message': 'Verification failed.',
            'error_codes': verification.get('error-codes', [])
        }), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
