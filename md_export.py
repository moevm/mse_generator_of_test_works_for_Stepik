import json
import download
import random
import os
import shutil

def process(course, test_name, var_qty=1, task_qty=5):
    file_names = []
    if not (os.path.exists('./md_works')):
        os.makedirs(os.path.join(os.curdir, './md_works'))
    else:
        shutil.rmtree('./md_works')
        os.makedirs(os.path.join(os.curdir, './md_works'))

    for var_num in range(var_qty):
        file_name = os.path.join('./md_works', test_name.replace(' ', '_') + '_var_{}'.format(var_num + 1) + '.md')
        file_names.append(file_name)
        
        with open(file_name, mode='w', encoding='utf8') as f:
            f.write('# ' + test_name + '  \n\n')
            f.write('## Вариант {}  \n\n'.format(var_num + 1))
            f.write('******\n\n')
            f.write('**ФИО:**\n\n')
            f.write('**Группа:**\n\n')
            f.write('**Дата:**\n\n')
            f.write('******\n\n')

            var = course.get_chosen()
            var = [var[i] for i in random.sample(range(len(var)), task_qty)]

            for num, step in enumerate(var):
                print(step.get_type())
                if step.get_type() == 'number':
                    number(f, step.get_path(), num + 1)
                elif step.get_type() == 'choice':
                    choiсe(f, step.get_path(), num + 1)
                else:
                    string(f, step.get_path(), num + 1)    

    return file_names

def choiсe(fp, step, num):
    src = open(step, mode='r')
    step = json.load(src)
    src.close()
    fp.write(str(num) + '. ' + step['block']['text'] + '  \n')

    for option in step['block']['source']['options']:
        fp.write('    ' + '- ' + option['text'] + '  \n')
    
    fp.write('\n')

def number(fp, step, num):
    src = open(step, mode='r')
    step = json.load(src)
    src.close()

    fp.write(str(num) + '. ' + step['block']['text'] + '*(ответом является число)*  \n')
    fp.write('    ' + '**Ответ:**  \n')

    fp.write('\n')

def string(fp, step, num):
    src = open(step, mode='r')
    step = json.load(src)
    src.close()
    
    fp.write(str(num) + '. ' + step['block']['text'] + '*(ответом является строка)*  \n')
    fp.write('    ' + '**Ответ:**  \n')

    fp.write('\n')
