import os
import json
import requests
import datetime
import sys
import re
from weasyprint import HTML


class Course():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.modules = []  # List of Module objects
        self.path = ''

    def get_id(self):
        return self.id

    def get_modules(self):
        return self.modules

    def get_name(self):
        return self.name

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def get_chosen(self):
        chosen_steps = []
        for module in self.modules:
            if module.get_status():
                for lesson in module.get_lessons():
                    if lesson.get_status():
                        for step in lesson.get_steps():
                            if step.get_status():
                                chosen_steps.append(step)
        return chosen_steps

class Module():
    def __init__(self, name):
        self.name = name
        self.path = ''
        self.lessons = []  # list of Lesson object
        self.isChoose = False

    def get_lessons(self):
        return self.lessons

    def get_name(self):
        return self.name

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def choose(self):
        self.isChoose = True
        for lesson in self.lessons:
            lesson.choose()

    def unchoose(self):
        self.isChoose = False
        for lesson in self.lessons:
            lesson.unchoose()

    def get_status(self):
        return self.isChoose

class Lesson():
    def __init__(self, module, name):
        self.name = name
        self.path = ''
        self.steps = []  # list of Step object

        # True if module parent is choosen
        if module.isChoose:
            self.isChoose = True
        else:
            self.isChoose = False

    def get_steps(self):
        return self.steps

    def get_name(self):
        return self.name

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def choose(self):
        self.isChoose = True
        for step in self.steps:
            step.choose()

    def unchoose(self):
        self.isChoose = False
        for step in self.steps:
            step.unchoose()

    def get_status(self):
        return self.isChoose

class Step():
    def __init__(self, lesson, type):
        self.path = ''
        self.type = type  # string, choise, ...

        # True if module parent is choosen
        if lesson.isChoose:
            self.isChoose = True
        else:
            self.isChoose = False
        self.answer = ''    

    def get_type(self):
        return self.type

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def choose(self):
        self.isChoose = True

    def unchoose(self):
        self.isChoose = False

    def get_status(self):
        return self.isChoose

    def set_answer(self, answer):
        self.answer = answer

    def get_answer(self):
        return self.answer       

def fetch_object(obj_class, obj_id, token):
    api_url = '{}/api/{}s/{}'.format('https://stepik.org', obj_class, obj_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response['{}s'.format(obj_class)][0]

def fetch_objects(obj_class, obj_ids, token):
    objs = []
    # Fetch objects by 30 items,
    # so we won't bump into HTTP request length limits
    step_size = 30
    for i in range(0, len(obj_ids), step_size):
        obj_ids_slice = obj_ids[i:i + step_size]
        api_url = '{}/api/{}s?{}'.format('https://stepik.org', obj_class,
                                         '&'.join('ids[]={}'.format(obj_id)
                                                  for obj_id in obj_ids_slice))
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}
                                ).json()
        objs += response['{}s'.format(obj_class)]
    return objs

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def download_course(token, course_id):
    plan = ''
    token = token
    course = fetch_object('course', course_id, token=token)
    _course = Course(course['id'], course['title'])
    sections = fetch_objects('section', course['sections'], token=token)  # Модули
    
    for section in sections:  # Итерация по модулям
        unit_ids = section['units']
        units = fetch_objects('unit', unit_ids, token=token)  # Уроки
        _module = Module(section['title'])
        _course.modules.append(_module)
        for unit in units:  # Итерация по урокам
            lesson_id = unit['lesson']
            lesson = fetch_object('lesson', lesson_id, token=token)
            _lesson = Lesson(_module, lesson['title'])
            _module.lessons.append(_lesson)

            step_ids = lesson['steps']
            steps = fetch_objects('step', step_ids, token=token)  # Степы
            # print(steps[0])
            plan += lesson['title'] + '\n' + steps[0]['block']['text'] + '<div><br></div>'         
            for step in steps:  # Итерация по степам
                if step['block']['name'] in ('choice', 'number', 'string'):
                    _step = Step(_lesson, step['block']['name'])
                    step_source = fetch_object('step-source', step['id'], token=token)
                    if step_source['block']['name'] == 'choice':
                        for opt in step_source['block']['source']['options']:
                            if opt['is_correct']:
                                _step.set_answer(opt['text'])
                    elif step_source['block']['name'] == 'number':
                        _step.set_answer(step_source['block']['source']['options'][0]['answer'])
                    elif step_source['block']['name'] == 'string':
                        _step.set_answer(step_source['block']['source']['pattern'])
                    _lesson.steps.append(_step)
                    path = [
                        '{}'.format(str(course['id']).zfill(2)),
                        '{}_{}'.format(str(section['position']).zfill(2), str(section['title']).replace(' ','_')),
                        '{}_{}'.format(str(unit['position']).zfill(2), str(lesson['title']).replace(' ','_')),
                        '{}_{}_{}.step'.format(lesson['id'], str(step['position']).zfill(2), step['block']['name'])
                    ]

                    if not _step.get_path():
                        _step.set_path(os.path.join(os.curdir, *path))
                    if not _lesson.get_path():
                        _lesson.set_path(os.path.join(os.curdir, *path[:3]))
                    if not _module.get_path():
                        _module.set_path(os.path.join(os.curdir, *path[:2]))
                    if not _course.get_path():
                        _course.set_path(os.path.join(os.curdir, path[0]))

                    try:
                        os.makedirs(os.path.join(os.curdir, *path[:-1]))
                    except:
                        pass
                    filename = os.path.join(os.curdir, *path)
                    f = open(filename, 'w')
                    data = {
                        'block': step_source['block'],
                        'id': str(step['id']),
                        'time': datetime.datetime.now().isoformat()
                    }

                    data['block']['text'] = step['block']['text']
                    f.write(json.dumps(data))
                    f.close()
    html = HTML(string=plan)
    html.write_pdf('plan.pdf')
    return _course