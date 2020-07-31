from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import admin_models
from config import *
from dotenv import load_dotenv
from app.command import db_init
from app.utils import generate_random_salt, decode
import random, base64

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # TestConfig 고정
        self.app = create_app(TestConfig)
        # if os.environ.get("CURRENT_ENV") == "Test":
        #     self.app = create_app(TestConfig)
        # elif os.environ.get("CURRENT_ENV") == "LocalDevelop":
        #     self.app = create_app(LocalDevelopConfig)
        # elif os.environ.get("CURRENT_ENV") == "HerokuDevelop":
        #     self.app = create_app(HerokuDevelopConfig)
        # else:
        #     raise EnvironmentError

        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_encryption(self):
        for i in range(10):
            password = str(random.randint(1000, 10000))
            salt = str(generate_random_salt())
            pasalt = base64.b64encode((password + salt).encode("UTF-8")).decode("UTF-8")
            result = decode(pasalt, salt)
            self.assertEqual(password, result)

if __name__ == '__main__':
    unittest.main(verbosity=2)