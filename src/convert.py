import json
import download
import random
import os
import shutil
from weasyprint import HTML


def generating_works(course, test_name, var_qty=1, task_qty=5):
    pdf_path = os.path.join(os.curdir, '{}'.format(course.get_id()), 'data/pdf') # папка для pdf
    answers_path = os.path.join(os.curdir, '{}'.format(course.get_id()), 'data/answers') # папка для ответов
    archive_path = os.path.join(os.curdir, '{}'.format(course.get_id()), 'works_archive') # папка для архива
    
    if not (os.path.exists(pdf_path)):
        os.makedirs(pdf_path)
    else:
        shutil.rmtree(pdf_path)
        os.makedirs(pdf_path)
    if not (os.path.exists(answers_path)):
        os.makedirs(answers_path)
    else:
        shutil.rmtree(answers_path)
        os.makedirs(answers_path)
    all_answers_file_name = os.path.join(answers_path, 'all_answers.txt')
    aaf = open(all_answers_file_name, 'w')
    aaf.close()
    aaf = open(all_answers_file_name, 'a') 
    aaf.write("Работа: {}".format(test_name) + '\n\n')
    for var_num in range(var_qty):
        var_string = ""
        answers_file_name = os.path.join(answers_path, 'answers' + '_var_{}'.format(var_num + 1) + '.txt')
        aaf.write('Вариант {}'.format(var_num + 1) + ': \n')

        var_string += '<h1>{}</h1>'.format(test_name) + '<h2>Вариант {}</h2>'.format(var_num + 1) + '<h3>ФИО:</h3>'
        var_string += '<h3>Группа:</h3>' + '<h3>Дата</h3><br>'
        var = course.get_chosen()
        while len(var) < task_qty:
            var += var
            
        var = [var[i] for i in random.sample(range(len(var)), task_qty)]

        af = open(answers_file_name, 'w')
        af.close()
        af = open(answers_file_name, 'a')
        af.write('Вариант {}.'.format(var_num + 1) + '\n')
        for num, step in enumerate(var):
            if step.get_type() == 'number':
                var_string += number(step, num)
            elif step.get_type() == 'choice':
                var_string += choice(step, num)
            else:
                var_string += string(step, num)
            af.write('{}. '.format(num + 1) + step.get_answer() + '\n')
            aaf.write('{}. '.format(num + 1) + step.get_answer() + '\n')
        aaf.write('\n\n')  
        html = HTML(string=var_string)
        pdf_file_name = os.path.join(pdf_path,'{}_var_{}.pdf'.format(test_name, var_num + 1))
        html.write_pdf(pdf_file_name)
        ret = []
        ret.append(archive_path)
        ret.append(course.get_id())
    return ret

def choice(step, num):
    step_string = ""
    src = open(step.get_path(), 'r')
    _step = json.load(src)
    src.close()
    step_string += '<div><p>' + str(num + 1) + '. ' + _step['block']['text'] + '</p><ol>'
    for option in _step['block']['source']['options']:
        step_string += '<li>' + '- ' + option['text'] + '</li>'
    step_string += '</ol></div>'
    return step_string

def number(step, num):
    step_string = ""
    src = open(step.get_path(), 'r')
    _step = json.load(src)
    src.close()
    step_string += '<div><p>' + str(num + 1) + '. ' + _step['block']['text'] + '</p>' + '<p><i>(ответом является число)</i></p>'
    step_string += '    ' + 'Ответ:  \n</div>'
    return step_string

def string(step, num):
    step_string = ""
    src = open(step.get_path(), 'r')
    _step = json.load(src)
    src.close()
    step_string += '<div><p>' + str(num + 1) + '. ' + _step['block']['text'] + '</p>' + '<p><i>(ответом является строка)</i></p>'
    step_string += '    ' + 'Ответ:  \n</div>'
    return step_string

def archive(archive_path, course_id):
    if (os.path.exists(archive_path)):
        shutil.rmtree(archive_path)
    shutil.make_archive(os.path.join(archive_path, 'stepik_works'), 'zip', os.path.join(os.curdir, '{}'.format(course_id), 'data'))
    return os.path.join(archive_path, 'stepik_works.zip')
