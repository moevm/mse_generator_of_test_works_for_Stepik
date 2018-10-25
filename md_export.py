import json
import download
import random

def process(course, test_name, var_qty=1, task_qty=5):
    file_names = []
    for var_num in range(var_qty):
        file_name = test_name.replace(' ', '_') + '_var_{}'.format(var_num + 1) + '.md'
        file_names.append(file_name)
        
        with open(file_name, mode='w', encoding='utf8') as f:
            f.write('# ' + test_name + '  \n\n')
            f.write('## Вариант {}  \n\n'.format(var_num + 1))
            f.write('******\n\n')
            f.write('<table class="w3-table-all w3-large w3-centered"><tr><th>Фио</th><th>Группа</th><th>Дата</th></tr><tr><td style="opacity: 0.05;">*************************</td><td style="opacity: 0.05;">****</td><td style="opacity: 0.05;">**********</td></tr></table>\n\n')
            f.write('******\n\n')

            var = course.get_chosen()
            var = [var[i] for i in random.sample(range(len(var)), task_qty)]

            for num, step in enumerate(var):
                if step.get_type() == 'number':
                    number(f, step.get_path(), num + 1)
                elif step.get_type() == 'choice':
                    choiсe(f, step.get_path(), num + 1)
                elif step.get_type == 'string':
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

    fp.write(str(num) + '. ' + step['block']['text'] + '  \n')
    fp.write('*(ответом является число)*  \n')
    fp.write('    ' + '**Ответ:**  \n')

    fp.write('\n')

def string(fp, step, num):
    src = open(step, mode='r')
    step = json.load(src)
    src.close()
    
    fp.write(str(num) + '. ' + step['block']['text'] + '  \n')
    fp.write('*(ответом является строка)*  \n')
    fp.write('    ' + '**Ответ:**  \n')

    fp.write('\n')
