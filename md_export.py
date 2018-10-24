import json
import download

def process(course, test_name, var_qty=1, task_qty=10):
    file_name = test_name.replace(' ', '_') + '.md'
    with open(file_name, mode='w', encoding='utf8') as f:
        f.write('# ' + test_name + '\n')
        f.write('## Вариант 1\n')
        f.write('**ФИО**___________________________________\n')
        f.write('**Группа**_____\n')
        f.write('**Дата**__________\n')
        for num, step in enumerate(course.get_chosen()):
            if step.get_type() == 'number':
                number(f, step.get_path(), num + 1)
            elif step.get_type() == 'choice':
                choiсe(f, step.get_path(), num + 1)
            elif step.get_type == 'string':
                string(f, step.get_path(), num + 1)    

    return file_name

def choiсe(fp, step, num):
    src = open(step, mode='r')
    step = json.load(src)
    src.close()

    fp.write(str(num) + '. ' + step['block']['text'] + '\n')

    for option in step['block']['source']['options']:
        fp.write('\t' + '- ' + option['text'] + '\n')

def number(fp, step, num):
    src = open(step, mode='r')
    step = json.load(src)
    src.close()

    fp.write(str(num) + '. ' + step['block']['text'].replace('<p>', '').replace('</p>', '') + '\n')
    fp.write('*(ответом является число)*\n')
    fp.write('\t' + '- **Ответ:** _____________________\n')

def string(fp, step, num):
    src = open(step, mode='r')
    step = json.load(src)
    src.close()

    fp.write(str(num) + '. ' + step['block']['text'].replace('<p>', '').replace('</p>', '') + '\n')
    fp.write('*(ответом является строка)*\n')
    fp.write('\t' + '- **Ответ:** _____________________\n')
