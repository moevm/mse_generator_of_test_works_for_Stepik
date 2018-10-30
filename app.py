# -*- encoding: utf-8 -*-

import sys

from flask import Flask, render_template, request, send_file, session, redirect, url_for, make_response
from functools import wraps, update_wrapper
from datetime import datetime
import user
import download
import md_export
import os
import markdown
import pickle
from xhtml2pdf import pisa

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
app.secret_key = 'A0Zr37w/3rX R~XHH-jmm]LSX/,?RT'

@app.route('/')
@nocache
def index():
    if 'token' in session:
        return redirect(url_for('courses'))
    else:    
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
            if not os.path.exists(str(course_id)) or not os.path.isdir(str(course_id)):
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
    
    for module in course.get_modules():
        if module.get_name() == request.form['module']:
            module.choose()

    test_name = md_export.process(course, request.form['name'], request.form['var_qty'], request.form['task_qty'])

    # markdown.markdownFromFile(input=test_name, output=test_name.replace('.md', '.html'))
    
    # output = open(test_name.replace('.md', '.pdf'), mode='w+b')
    # src = open(test_name.replace('.md', '.html'), mode='r', encoding='utf8')
    
    # pisa.CreatePDF(src.read(), dest=output)
    
    # output.close()
    # src.close()

    return send_file(test_name, mimetype='text/markdown')
    #return send_file(test_name.replace('.md', '.html'), mimetype='text/html')
    #return send_file('Контрольная.pdf', mimetype='application/pdf')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)