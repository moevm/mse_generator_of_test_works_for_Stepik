from app import app
from flask import url_for
import unittest
import json

with open('config.json', 'r') as f:
    config = json.load(f)
    auth_path = config['auth_path']

class BasicTestCase(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()


    def test_index(self):
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    
    def test_auth_req(self):
        response = self.app.get(f'{auth_path}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    

    def test_courses_req(self):
        response = self.app.get('/courses', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    '''
    def test_generate_req(self):
        form=dict()
        form['course_id'] = 1
        form['module'] = ('test1', 'test2')
        form['name'] = "testname"
        form['var_qty'] = 1
        form['task_qty'] = 1
        response = self.app.post('/generate', data=form,follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    '''

    def test_plan_req(self):
        response = self.app.get('/plan', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_check_req(self):
        response = self.app.get('/check', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_logout_req(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()