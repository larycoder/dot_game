from flask_testing import TestCase
from dot_game import app, db
from install.init_database import install as data_install

class BaseTestCase(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        self._BaseTestCase_database_name = db.session.bind.url.database.split("/")[-1]
        self.assertTrue(self._BaseTestCase_database_name == "test.db")
        if self._BaseTestCase_database_name == "test.db":
            db.create_all()
            data_install()
    
    def tearDown(self):
        if self._BaseTestCase_database_name == "test.db":
            db.session.remove()
            db.drop_all()