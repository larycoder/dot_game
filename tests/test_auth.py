from tests.base import BaseTestCase
from tests.helper import register, login

import json

class TestAuthBlueprint(BaseTestCase):

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

