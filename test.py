from datetime import datetime, timedelta
import unittest
from myapp import create_app, db
from myapp.models import mymodel
from config import Config


class TestConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.myapp.app_context()
        self.app_context.push()
        db.create_all()

    def test_method(self):
        # 단위 테스트 작성
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)