from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import mymodel
from config import *
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class MyTestCase(unittest.TestCase):
    def setUp(self):
        if os.environ.get("CURRENT_ENV") == "Test":
            self.app = create_app(TestConfig)
        elif os.environ.get("CURRENT_ENV") == "LocalDevelop":
            self.app = create_app(LocalDevelopConfig)
        elif os.environ.get("CURRENT_ENV") == "HerokuDevelop":
            self.app = create_app(HerokuDevelopConfig)
        else:
            raise EnvironmentError

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_method(self):
        # Heroku DB 환경에서는 db connect 있는 테스트 작성 x
        pass
    
    def test_solve_hash(self):
        sample = mymodel.MyModel(username="move02", email="asdf@asdf.com", password="1234")
        self.assertTrue(sample.check_password("1234"))

if __name__ == '__main__':
    unittest.main(verbosity=2)