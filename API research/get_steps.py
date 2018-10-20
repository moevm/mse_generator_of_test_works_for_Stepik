# Run with Python 3
# Saves all step sources into foldered structure
import os
import json
import requests
import datetime
import sys

# 3. Call API (https://stepik.org/api/docs/) using this token.
def fetch_object(obj_class, obj_id):
    api_url = '{}/api/{}s/{}'.format(api_host, obj_class, obj_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response['{}s'.format(obj_class)][0]


def fetch_objects(obj_class, obj_ids):
    objs = []
    # Fetch objects by 30 items,
    # so we won't bump into HTTP request length limits
    step_size = 30
    for i in range(0, len(obj_ids), step_size):
        obj_ids_slice = obj_ids[i:i + step_size]
        api_url = '{}/api/{}s?{}'.format(api_host, obj_class,
                                         '&'.join('ids[]={}'.format(obj_id)
                                                  for obj_id in obj_ids_slice))
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}
                                ).json()
        objs += response['{}s'.format(obj_class)]
    return objs


if __name__ == "__main__":
    # Enter parameters below:
    # 1. Get your keys at https://stepik.org/oauth2/applications/
    # (client type = confidential, authorization grant type = client credentials)
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    api_host = 'https://stepik.org'
    course_id = sys.argv[3]

    # 2. Get a token
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('https://stepik.org/oauth2/token/',
                             data={'grant_type': 'client_credentials'},
                             auth=auth)
    token = response.json().get('access_token', None)
    if not token:
        print('Unable to authorize with provided credentials')
        exit(1)

    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])  # Модули

    for section in sections:  # Итерация по модулям
        '''
        В ходе проверок принтами было выявлено, что поле "is_exam" имеется только у section
        так что если нужно отслеживать существующие контрольные, то их надо делать в виде модулей(?)
        '''
        unit_ids = section['units']
        units = fetch_objects('unit', unit_ids)  # Уроки

        for unit in units:  # Итерация по урокам
            lesson_id = unit['lesson']
            lesson = fetch_object('lesson', lesson_id)

            step_ids = lesson['steps']
            steps = fetch_objects('step', step_ids)  # Степы

            for step in steps:  # Итерация по степам
                #if step['block']['name'] == 'choice':  # В этом месте можно отбирать нужные степы(по типу задания)
                step_source = fetch_object('step-source', step['id'])
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