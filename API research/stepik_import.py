import os
import json
import requests
import datetime
import sys

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
    sections = fetch_objects('section', course['sections'], token=token)  # Модули

    for section in sections:  # Итерация по модулям
        unit_ids = section['units']
        units = fetch_objects('unit', unit_ids, token=token)  # Уроки

        for unit in units:  # Итерация по урокам
            lesson_id = unit['lesson']
            lesson = fetch_object('lesson', lesson_id, token=token)

            step_ids = lesson['steps']
            steps = fetch_objects('step', step_ids, token=token)  # Степы

            for step in steps:  # Итерация по степам
                # if step['block']['name'] == 'choice':  # В этом месте можно отбирать нужные степы(по типу задания)
                step_source = fetch_object('step-source', step['id'], token=token)
                path = [
                    '{} {}'.format(str(course['id']).zfill(2), course['title']),
                    '{} {}'.format(str(section['position']).zfill(2), section['title']),
                    '{} {}'.format(str(unit['position']).zfill(2), lesson['title']),
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
    return dir_path
