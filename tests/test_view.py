from tests.base import BaseTestCase
from tests.helper import register, login

import json

class TestViewBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register(self, 'hieplnc', 'hieplnc')
            data = json.loads(response.data.decode())

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        """ Test for user login """
        # user registration
        self.test_registration()

        # user login
        response = login(self, 'hieplnc', 'hieplnc')
        data = json.loads(response.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_guiline_import_with_code(self):
        """ Test user import new guideline """
        # register data
        self.test_registration()

        # login
        response_login = login(self, 'hieplnc', 'hieplnc')
        data = json.loads(response_login.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response_login.content_type == 'application/json')
        self.assertEqual(response_login.status_code, 200)

        # test import guideline
        response = self.client.post(
            "/core/guideline/import",
            headers = dict(
                Authorization = "Bearer " + json.loads(response_login.data.decode())['auth_token']
            ),
            data = json.dumps(dict(
                version = "0.1.0",
                name = "Test",
                description = "this is test",
                code = "function MyFunction():{pass;}"
            )),
            content_type = "application/json"
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully import instruction.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)
    
    def test__user_get_guideline_lists(self):
        """ Test user get list of guideline """
        # add guideline to db
        self.test_guiline_import_with_code()

        # login
        response_login = login(self, 'hieplnc', 'hieplnc')
        data = json.loads(response_login.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response_login.content_type == 'application/json')
        self.assertEqual(response_login.status_code, 200)

        # get list guideline
        response = self.client.get(
            '/core/guideline/list',
            headers = dict(
                Authorization = 'Bearer ' + json.loads(response_login.data.decode())['auth_token']
            )
        )        

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully get guideline.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(isinstance(data['guideline'], list))
        self.assertTrue(response_login.content_type == 'application/json')
        self.assertEqual(response_login.status_code, 200)



