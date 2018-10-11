from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # 1. Get your keys at https://stepik.org/oauth2/applications/
    # (client type = confidential, authorization grant type = client credentials)
    client_id = request.form['client_id']
    client_secret = request.form['client_secret']

    # 2. Get a token
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('https://stepik.org/oauth2/token/',
                            data={'grant_type': 'client_credentials'},
                            auth=auth)
    token = response.json().get('access_token', None)
    if not token:
        return 'Unable to authorize with provided credentials'
    else:
        api_url = 'https://stepik.org/api/stepics/1'  # should be stepic with "c"!
        response = requests.get(api_url, headers={'Authorization': 'Bearer '+ token}).json()

        user = response.get('users', None)
        name = user[0]['first_name'] +' ' + user[0]['last_name']
        return name

if __name__ == '__main__':
    app.run(debug=True)