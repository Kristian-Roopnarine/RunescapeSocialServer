from flask_testing import TestCase
import sys

sys.path.append('./')
from app.models import db
import app

TEST_DB = "test.db"

class BaseTestCase(TestCase):
    def create_app(self):
        thisapp = app.create_app()
        thisapp.config['TESTING'] = True
        thisapp.config['DEBUG'] = False
        thisapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        return thisapp

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass