import os
import unittest
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent / 'src')
sys.path.insert(0, src_path)

# Load environment variables
load_dotenv()

from src.__init__ import create_app, db

class TestConfig(unittest.TestCase):
    def setUp(self):
        """Set up test application"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up test database"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_config_loading(self):
        """Test if the app loads the testing configuration"""
        self.assertTrue(self.app.config['TESTING'])
        self.assertEqual(
            self.app.config['SQLALCHEMY_DATABASE_URI'],
            os.getenv('TEST_DATABASE_URL')
        )

if __name__ == '__main__':
    unittest.main()