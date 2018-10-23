import sys

from flask import Flask, render_template, request, send_file, session, redirect, url_for
import user
import download
import md_export
import os
import markdown

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

@app.route('/course')
def course():
    if 'token' in session:
        course_id = request.args.get('id', default=None, type=int)
        if not course_id:
            return redirect(url_for('courses'))
        else:
            if os.path.exists(str(course_id)) and os.path.isdir(str(course_id)):
                return 'Already downloaded ' + str(course_id)
            else:
                return 'Will be downloaded'
                #path = download.download_course(session['token'], course_id)
    else:
        return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    #TODO generating
    # return html with generated test
    return send_file('tmp.html', mimetype='text/html')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)