# tests/helper.py

import json

def register(self, user, password):
    return self.client.post(
        '/core/register',
        data = json.dumps(dict(
            user = user,
            password = password
        )),
        content_type = 'application/json'
    )

def login(self, user, password):
    return self.client.post(
        '/core/login',
        data = json.dumps(dict(
            user = user,
            password = password
        )),
        content_type = 'application/json'
    )