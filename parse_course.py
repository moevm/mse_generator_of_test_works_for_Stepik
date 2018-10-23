import os
import json
import requests
import datetime
import sys


class Course():
    def __init__(self, id):
        self.id = id
        self.modules = []  # List of Module objects


class Module():
    def __init__(self, name):
        self.name = name
        self.path = 'path'
        self.lessons = []  # list of Lesson object
        self.isChoose = False


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

    def get_name(self):
        return self.name

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path


class Step():
    def __init__(self, lesson, type):
        self.path = ''
        self.type = type  # string, choise, ...

        # True if module parent is choosen
        if lesson.isChoose:
            self.isChoose = True
        else:
            self.isChoose = False

    def get_type(self):
        return self.type

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

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

def download_course(token, course_id):
    token = token
    course = fetch_object('course', course_id, token=token)
    _course = Course(course['id'])
    print(_course.id)
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

            for step in steps:  # Итерация по степам
                _step = Step(_lesson, step['block']['name'])
                _lesson.steps.append(_step)
                step_source = fetch_object('step-source', step['id'], token=token)
                path = [
                    '{}'.format(str(course['id']).zfill(2)),
                    '{}_{}'.format(str(section['position']).zfill(2), str(section['title']).replace(' ','_')),
                    '{}_{}'.format(str(unit['position']).zfill(2), str(lesson['title']).replace(' ','_')),
                    '{}_{}_{}.step'.format(lesson['id'], str(step['position']).zfill(2), step['block']['name'])
                ]
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
                f.write(json.dumps(data))
                f.close()
                print(filename)
    dir_path = os.path.join(os.curdir, path[0])
    for module in _course.modules:
        print(module.name)
        for lesson in module.lessons:
            print("----", lesson.name)
            for step in lesson.steps:
                print("--------", step.type)
    return _course