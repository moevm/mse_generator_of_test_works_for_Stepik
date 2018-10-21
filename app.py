import sys

from flask import Flask, render_template, request, send_file, session, redirect, url_for
import user
import download
import md_export
import os

app = Flask(__name__)
app.secret_key = 'A0Zr37w/3rX R~XHH-jmm]LSX/,?RT'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    token = user.get_token(request.form['client_id'], request.form['client_secret'])

    if not token:
        return 'Unable to authorize with provided credentials'
    else:
        session['token'] = token
        return redirect(url_for('courses'))

@app.route('/courses')
def courses():
    if 'token' in session:
        name = user.get_user_name(session['token'])
        courses = user.get_admin_courses(session['token'])

        return render_template('user_info.html', courses=courses, name=name)
    else:
        return redirect(url_for('index'))

@app.route('/course', methods=['POST'])
def course():
    if 'token' in session:
        path = download.download_course(session['token'], request.form['id'])
        return 'Downloaded course!'
    else:
        return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    return send_file('tmp.pdf', mimetype='application/pdf')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)