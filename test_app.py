import unittest
from unittest.mock import MagicMock
import falcon
from falcon import testing
from resource import UserResource


class TestUserResource(testing.TestCase):
    def setUp(self):
        # Mock the UserRepository
        self.user_repository = MagicMock()

        # Create an instance of UserResource with the mocked repository
        self.user_resource = UserResource(self.user_repository)

        # Create a Falcon app and add the route
        self.app = falcon.App()
        self.app.add_route('/users', self.user_resource)

        # Use the testing client for the app
        self.client = testing.TestClient(self.app)

    def test_create_user_success(self):
        user_data = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
        self.user_repository.create_user.return_value = 1

        response = self.client.simulate_post('/users', json=user_data)

        self.assertEqual(response.status, falcon.HTTP_201)
        self.assertEqual(response.json["message"], "User created successfully.")
        self.user_repository.create_user.assert_called_once()

    def test_create_user_validation_error(self):
        invalid_user_data = {"name": "John Doe", "email": "invalid_email", "age": -5}

        response = self.client.simulate_post('/users', json=invalid_user_data)

        self.assertEqual(response.status, falcon.HTTP_400)
        self.assertIn("Invalid Input", response.json["message"])

    def test_create_user_duplicate_email(self):
        user_data = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
        self.user_repository.create_user.side_effect = ValueError("Email 'john.doe@example.com' is already in use.")

        response = self.client.simulate_post('/users', json=user_data)

        self.assertEqual(response.status, falcon.HTTP_409)
        self.assertEqual(response.json["message"], "Email 'john.doe@example.com' is already in use.")

    def test_get_user_by_email_success(self):
        self.user_repository.get_user_by_email.return_value = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30
        }

        response = self.client.simulate_get('/users?email=john.doe@example.com')

        self.assertEqual(response.status, falcon.HTTP_200)
        self.assertEqual(response.json["name"], "John Doe")

    def test_get_user_by_email_not_found(self):
        self.user_repository.get_user_by_email.return_value = None

        response = self.client.simulate_get('/users?email=nonexistent@example.com')

        self.assertEqual(response.status, falcon.HTTP_404)
        self.assertEqual(response.json["message"], "User not found.")


if __name__ == '__main__':
    unittest.main()
