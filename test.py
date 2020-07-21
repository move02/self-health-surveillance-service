from datetime import datetime, timedelta
import unittest
from myapp import create_app, db
from myapp.models import mymodel
from config import Config


class TestConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite://'

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_method(self):
        # 단위 테스트 작성
        mymodel.MyModel.query.all()
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)