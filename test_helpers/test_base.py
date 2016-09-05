from flask_testing import TestCase
from config import TestConfiguration
from pipig import app, db


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        app.config.from_object(TestConfiguration)

        return app

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        app.config['TESTING'] = True


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
