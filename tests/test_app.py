import unittest
from app import app, db, PasswordManager


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password Manager App", response.data)

    def test_add_details(self):
        response = self.client.post(
            "/add",
            data={
                "title": "Test",
                "email": "test@example.com",
                "site_url": "example.com",
                "site_password": "password",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Check if it redirects after adding data
        added_data = PasswordManager.query.filter_by(title="Test").first()
        self.assertIsNotNone(added_data)

    def test_export_data(self):
        response = self.client.get("/export")
        self.assertEqual(
            response.status_code, 200
        )  # Check if export route returns a successful response


if __name__ == "__main__":
    unittest.main()
