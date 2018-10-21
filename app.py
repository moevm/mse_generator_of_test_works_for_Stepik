import sys

from flask import Flask, render_template, request
import requests
import getting_courses
from getting_courses import getting_courses

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    client_id = request.form['client_id']
    client_secret = request.form['client_secret']

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('https://stepik.org/oauth2/token/',
                            data={'grant_type': 'client_credentials'},
                            auth=auth)
    token = response.json()['access_token']

    if not token:
        return 'Unable to authorize with provided credentials'
    else:
        courses = getting_courses.get_admin_courses(token)
        return render_template('user_info.html', courses=courses)

if __name__ == '__main__':
    app.run(debug=True)