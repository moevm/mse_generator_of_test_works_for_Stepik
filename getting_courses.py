# coding=utf-8

import requests
import json

# 3. Call API (https://stepik.org/api/docs/) using token.
# Generator definition for iterating over pages
def list_pages(api_url, obj_class):
    has_next = True
    page = 1
    if '?' in api_url:
        connector = '&'
    else:
        connector = '?'
    while has_next:
        response = requests.get(api_url + '{}page={}'.format(connector, page),
                                headers={'Authorization': 'Bearer ' + token}).json()
        yield response[obj_class]
        page += 1
        has_next = response['meta']['has_next']


# Access to any API method
def fetch_object(obj_class, query_string=''):
    api_url = '{}/api/{}{}'.format('https://stepik.org', obj_class, query_string)
    response = list_pages(api_url, obj_class)
    return [obj for page in response for obj in page]


# Information about course sections
def get_sections(course_sections):
    qs = '?ids[]=' + '&ids[]='.join([str(cs) for cs in course_sections])    # Example of multiple IDs call
    sections = fetch_object('sections', qs)
    return sections


# Information about enrolled courses
def get_enrolled_courses():
    courses = fetch_object('courses', '?enrolled=true')
    for course in courses:
        course['sections'] = get_sections(course['sections'])
    return courses

# Return list of courses dict
def get_admin_courses(token):

    # getting user id
    r = json.loads(requests.get('https://stepik.org/api/stepics/1', headers={'Authorization': 'Bearer ' + token}).text)
    user_id = r['users'][0]['id']

    # Retrieving course information
    courses = get_enrolled_courses()
    admin_courses = []

    for course in courses:
        for instructor_id in course['instructors']:
            if instructor_id == user_id:
                admin_courses.append(course)
                break

    return admin_courses

