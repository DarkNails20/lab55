import unittest
import requests


BASE_URL = "http://127.0.0.1:5000"


class APISecurityTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        response = requests.get(
            BASE_URL + "/api/users",
            timeout=5
        )

        if response.status_code != 200:
            raise RuntimeError(
                "Flask API is not running. "
                "Start it with: python app.py"
            )

    def test_get_users(self):
        response = requests.get(
            BASE_URL + "/api/users",
            timeout=5
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_user(self):
        payload = {
            "name": "Security Test User",
            "email": "security@example.com"
        }

        response = requests.post(
            BASE_URL + "/api/users",
            json=payload,
            timeout=5
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            response.json()["email"],
            payload["email"]
        )

    def test_sql_injection_negative(self):
        payload = {
            "name": "' OR '1'='1",
            "email": "sqli-test@example.com"
        }

        response = requests.post(
            BASE_URL + "/api/users",
            json=payload,
            timeout=5
        )

        self.assertIn(
            response.status_code,
            (201, 400)
        )

        if response.status_code == 201:
            self.assertEqual(
                response.json()["name"],
                payload["name"]
            )

    def test_xss_negative(self):
        payload = {
            "name": "<script>alert('XSS')</script>",
            "email": "xss-test@example.com"
        }

        response = requests.post(
            BASE_URL + "/api/users",
            json=payload,
            timeout=5
        )

        self.assertIn(
            response.status_code,
            (201, 400)
        )

        if response.status_code == 201:
            self.assertEqual(
                response.json()["name"],
                payload["name"]
            )

    def test_invalid_json(self):
        response = requests.post(
            BASE_URL + "/api/users",
            data="not-json",
            headers={
                "Content-Type": "application/json"
            },
            timeout=5
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_nonexistent_user(self):
        response = requests.delete(
            BASE_URL + "/api/users/999999",
            timeout=5
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)