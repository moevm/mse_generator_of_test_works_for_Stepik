import sys

from flask import Flask, render_template, request
import user

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    app.token = user.get_token(request.form['client_id'], request.form['client_secret'])

    if not app.token:
        return 'Unable to authorize with provided credentials'
    else:
        name = user.get_user_name(app.token)
        courses = user.get_admin_courses(app.token)

        return render_template('user_info.html', courses=courses, name=name)

@app.route('/course', methods=['POST'])
def course():
    return 'TEST' + request.form['id']

if __name__ == '__main__':
    app.run(debug=True)