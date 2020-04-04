# Test cases for restful API
from RatingSystem import app
import unittest

class FlaskappTests(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
    def test_users_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/v1/users')
        print (result)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_products_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/v2/products')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_addusers_status_code(self):
        # sends HTTP POST request to the application
        # on the specified path
        result = self.app.post('/api/v1/users', data='{ "email": "ronaldrvera@jourrapide.com", "password": "juzahpei6e", "name":"Ronald R. Vera"}', content_type='application/json')
        print (result)
        # assert the status code of the response
        self.assertEquals(result.status_code, 201)

    def test_updusers_status_code(self):
        # sends HTTP PUT request to the application
        # on the specified path
        result = self.app.put('/api/v1/users/33', data='{"name":"Tagning", "email": "leolaLguertin@teleworm.us"}', content_type='application/json')
        # assert the status code of the response
        self.assertEquals(result.status_code, 200)
    def test_addproducts_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.post('/api/v2/products', data='{"name":"Tagning","id":"5" "price": "£100", "image:":"image.jpg", "category":"test", "description":"NULL"}', content_type='application/json')

        # assert the status code of the response
        self.assertEqual(result.status_code, 201)

    def test_delusers_status_code(self):
        # sends HTTP Delete request to the application
        # on the specified path
        result = self.app.delete('/api/v1/users', data='{"name":"Ronald R. Vera"}', content_type='application/json')
        print (result)
        # assert the status code of the response
        self.assertEquals(result.status_code, 200)
