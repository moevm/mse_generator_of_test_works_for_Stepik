# -*- coding: utf-8 -*-

import sys
sys.path.append('./src')

from distutils.util import strtobool
from flask import *
from functools import wraps, update_wrapper
from datetime import datetime
import user
import download
import os
import requests
import json
import pickle
import pathlib
import convert

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

app = Flask(__name__)
login_end_point = 'https://stepik.org/oauth2/authorize'

with open('config.json', 'r') as f:
    config = json.load(f)
    app.secret_key = config['secret_key']
    client_id = config['client_id']
    client_secret = config['client_secret']
    domen = config['domen']
    auth_path = config['auth_path']
    debug = config['debug']
    redirect_uri = f'{domen}{auth_path}'

@app.route('/')
@nocache
def index():
    return render_template('index.html',
        login_url=f'{login_end_point}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
    )

@app.route(auth_path)
def auth_code():
    code = request.args.get('code', default=None)
    if not code:
        flash('Ошибка авторизации!', 'error')
        flash('Ошибка получения кода для авторизации', 'info')
        return redirect(url_for('index'))
    
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('https://stepik.org/oauth2/token/',
                            data={
                                'grant_type': 'authorization_code',
                                'code': code,
                                'redirect_uri': redirect_uri
                                },
                            auth=auth)
    response = response.json()

    try:
        token = response['access_token']
    except:
        flash('Ошибка авторизации!', 'error')
        flash('Ошибка получения токена доступа', 'info')
        return redirect(url_for('index'))
    
    session.permanent = True
    app.permanent_session_lifetime = response['expires_in']
    session['token'] = token

    return redirect(url_for('courses'))

@app.route('/courses')
@nocache
def courses():
    if 'token' in session:
        if 'courses' in session and 'name' in session:
            name = session['name']
            courses_cookie = session['courses']
            courses = courses_cookie.split(';')
            courses = filter(lambda x: len(x) > 0, courses)
            courses = map(lambda x: {'title' : x.split('=')[0], 'id' : x.split('=')[1]}, courses)
        else:
            name = user.get_user_name(session['token'])
            courses = user.get_admin_courses(session['token'])

            courses_cookie = ''
            for course in courses:
                courses_cookie += course['title'] + '=' + str(course['id']) + ';'

            session['courses'] = courses_cookie
            session['name'] = name

        return render_template('user_info.html', courses=courses, name=name)
    else:
        return redirect(url_for('index'))

@app.route('/course')
@nocache
def course():
    if 'token' in session:
        course_id = request.args.get('id', default=None, type=int)
        
        if not course_id:
            return redirect(url_for('courses'))
        else:
            isDownload = strtobool(request.args.get('download', default=None))
            if isDownload:
                course = download.download_course(session['token'], course_id)
                with open(os.path.join(str(course_id), 'course_parser.dat'), mode='wb') as f:
                    pickle.dump(course, f)
            else:
                with open(os.path.join(str(course_id), 'course_parser.dat'), mode='rb') as f:
                    course = pickle.load(f)            
            
            return render_template('generation_setts.html', course=course, course_id=course_id)
    else:
        return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    with open(os.path.join(request.form['course_id'], 'course_parser.dat'), mode='rb') as f:
        course = pickle.load(f)

    selected_modules = request.form.getlist('module')

    for module in course.get_modules():
        if module.get_name() in selected_modules:
            module.choose()

    result = convert.generating_works(course, request.form['name'], 
                                int(request.form['var_qty']), int(request.form['task_qty']))

    if result:
        zip_path = convert.archive(course)
        return send_file(zip_path, 'application/zip')
    else:
        flash('Отсутствуют задания для генерации', 'error')
        return redirect(url_for('course', id=request.form['course_id'], download=False))
    
@app.route('/plan')
@nocache
def get_plan():
    if 'token' in session:
        course_id = request.args.get('id', default=None, type=int)
        
        if not course_id:
            return redirect(url_for('courses'))
        else:
            isDownload = strtobool(request.args.get('download', default=None))
            if isDownload:
                course = download.download_course(session['token'], course_id)
                with open(os.path.join(str(course_id), 'course_parser.dat'), mode='wb') as f:
                    pickle.dump(course, f)
                    
            return send_file(os.path.join(str(course_id), 'plan.pdf'), 'application/pdf')
    else:
        return redirect(url_for('index'))

@app.route('/check')
def get_save_status():
    if 'token' in session:
        course_id = request.args.get('id', default=None, type=int)
        if not course_id:
            return redirect(url_for('courses'))
        else:
            course_path = pathlib.Path(str(course_id))
            if os.path.exists(course_path):
                create_time = os.path.getctime(course_path)
                create_time = datetime.fromtimestamp(create_time)
                return jsonify({
                    'isSave': True,
                    'createDate': create_time
                })
            else:
                return jsonify({
                    'isSave': False,
                })
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0')