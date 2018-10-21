import json

def choise(fp, step, num):
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
