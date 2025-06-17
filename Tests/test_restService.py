import unittest
import json
import base64
import zlib
from Source.Controller.restService import app, users, grids, hash_password, User

class TestRestService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Clear users and grids before each test
        users.clear()
        grids.clear()
        # Create admin user
        users['admin'] = User('admin', hash_password('adminpass'), is_admin=True)
        # Login as admin
        response = self.app.post('/Cryptology/api/v1.0/login',
                               json={'username': 'admin', 'password': 'adminpass'})
        self.admin_token = response.json['token']
        self.admin_headers = {'X-Session-Token': self.admin_token}
    def test_user_management(self):
        # Create a new user
        response = self.app.post('/Cryptology/api/v1.0/users/create',
                               headers=self.admin_headers,
                               json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

        # Login as new user
        response = self.app.post('/Cryptology/api/v1.0/login',
                               json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        user_token = response.json['token']
        user_headers = {'X-Session-Token': user_token}

        # Try to create another user (should fail)
        response = self.app.post('/Cryptology/api/v1.0/users/create',
                               headers=user_headers,
                               json={'username': 'testuser2', 'password': 'testpass2'})
        self.assertEqual(response.status_code, 403)

        # Change password
        response = self.app.post('/Cryptology/api/v1.0/users/change-password',
                               headers=user_headers,
                               json={'current_password': 'testpass', 'new_password': 'newpass'})
        self.assertEqual(response.status_code, 200)

        # Try to login with old password (should fail)
        response = self.app.post('/Cryptology/api/v1.0/login',
                               json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 401)

        # Login with new password
        response = self.app.post('/Cryptology/api/v1.0/login',
                               json={'username': 'testuser', 'password': 'newpass'})
        self.assertEqual(response.status_code, 200)

    def test_grid_ownership(self):
        # Create a grid as admin
        response = self.app.get('/Cryptology/api/v1.0/createGrid',
                              headers=self.admin_headers,
                              query_string={'name': 'admin_grid', 'rows': 5, 'cols': 5})
        self.assertEqual(response.status_code, 200)

        # Create a new user
        response = self.app.post('/Cryptology/api/v1.0/users/create',
                               headers=self.admin_headers,
                               json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

        # Login as new user
        response = self.app.post('/Cryptology/api/v1.0/login',
                               json={'username': 'testuser', 'password': 'testpass'})
        user_token = response.json['token']
        user_headers = {'X-Session-Token': user_token}

        # Create a grid as user
        response = self.app.get('/Cryptology/api/v1.0/createGrid',
                              headers=user_headers,
                              query_string={'name': 'user_grid', 'rows': 99, 'cols': 99})
        self.assertEqual(response.status_code, 200)

        # Try to access admin's grid (should fail)
        response = self.app.get('/Cryptology/api/v1.0/display',
                              headers=user_headers,
                              query_string={'name': 'admin_grid'})
        self.assertEqual(response.status_code, 403)

        # Access own grid (should succeed)
        response = self.app.get('/Cryptology/api/v1.0/display',
                              headers=user_headers,
                              query_string={'name': 'user_grid'})
        self.assertEqual(response.status_code, 200)

        # Hide a message (should succeed)
        response = self.app.get('/Cryptology/api/v1.0/hide?',
                                headers=user_headers,
                                query_string={'name': 'user_grid', 'bandha':'rowByrowBandha', 'text':'this is the first mesage', 'x':0, 'y':0})
        self.assertEqual(response.status_code, 200)

        # Admin should be able to access all grids
        response = self.app.get('/Cryptology/api/v1.0/display',
                              headers=self.admin_headers,
                              query_string={'name': 'user_grid'})
        self.assertEqual(response.status_code, 200)

    def test_grid_operations(self):
        # Create a grid
        response = self.app.get('/Cryptology/api/v1.0/createGrid',
                              headers=self.admin_headers,
                              query_string={'name': 'test_grid', 'rows': 5, 'cols': 5})
        self.assertEqual(response.status_code, 200)

        # Test clear
        response = self.app.get('/Cryptology/api/v1.0/clear',
                              headers=self.admin_headers,
                              query_string={'name': 'test_grid'})
        self.assertEqual(response.status_code, 200)

        # Test export
        response = self.app.get('/Cryptology/api/v1.0/export',
                              headers=self.admin_headers,
                              query_string={'name': 'test_grid', 'filename': 'test_export.txt'})
        self.assertEqual(response.status_code, 200)

        # remove the grid
        response = self.app.get('/Cryptology/api/v1.0/removeGrid',
                              headers=self.admin_headers,
                              query_string={'name': 'test_grid'})
        self.assertEqual(response.status_code, 200)

        # Test import
        response = self.app.get('/Cryptology/api/v1.0/import',
                              headers=self.admin_headers,
                              query_string={'name': 'test_grid', 'filename': 'test_export.txt'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()