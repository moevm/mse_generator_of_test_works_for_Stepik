import sys

from flask import Flask, render_template, request, send_file, session, redirect, url_for
import user
import download
import md_export

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
        return redirect(url_for('/'))

@app.route('/course', methods=['POST'])
def course():
    if 'token' in session:
        download.download_course(session['token'], request.form['id'])
        # with open('test.md', mode='w', encoding='utf8') as fp:
        #     md_export.choise(fp, '48418/01 Тестовый Модуль 1/01 Тестовый Урок 1.1/183092_02_choice.step', 1)
        #     md_export.number(fp, '48418/01 Тестовый Модуль 1/01 Тестовый Урок 1.1/183092_03_number.step', 2)
        #     md_export.number(fp, '48418/01 Тестовый Модуль 1/01 Тестовый Урок 1.1/183092_04_string.step', 3)

        return send_file('test.md', mimetype='text/markdown')
    else:
        return redirect(url_for('/'))

if __name__ == '__main__':
    app.run(debug=True)