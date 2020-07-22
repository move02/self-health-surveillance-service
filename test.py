from datetime import datetime, timedelta
import unittest
from myapp import create_app, db
from myapp.models import mymodel
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
        elif os.environ.get("CURRENT_ENV") == "RemoteDevelop":
            self.app = create_app(RemoteDevelopConfig)
        else:
            self.app = create_app(RemoteDevelopConfig)

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_method(self):
        # 단위 테스트 작성
        mymodel.MyModel.query.all()
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)