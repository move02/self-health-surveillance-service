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
        # 단위 테스트 작성
        assert len(mymodel.MyModel.query.all()) >= 0
    
    def test_solve_hash(self):
        # 단위 테스트 작성
        sample = mymodel.MyModel.query.first()
        self.assertTrue(sample.check_password("1234"))

if __name__ == '__main__':
    unittest.main(verbosity=2)