import unittest
from dmLibrary import create_app
from dmLibrary.external.googleBook import GoogleBook
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestClass(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.gb = GoogleBook()
        logger.debug('logged from test_something')

    def tearDown(self):
        """Do the testing """
        pass

    def test_postCustomer(self):
        """
        test post new custoemr, try update, and delete it
        """
        data = {
            "name":"testName2 testLastName2",
            "email":"testTwo@gmail.com",
            "mobile":"0881231235"
        }

        response = self.client.post('/api/v1/customers',json=data)
        # logger.info(f"rawResp: {response.data}")
        self.assertEqual(response.status_code, 201)
        respData = response.get_json()
        self.assertEqual(respData["data"]['name'], data['name'])
        self.assertEqual(respData["data"]['email'], data['email'])
        self.assertEqual(respData["data"]['mobile'], data['mobile'])
        
        customer_id = respData["data"]["id"]
        # try update the title
        data = {
            "name":"chanename changelastname"
        }
        response = self.client.patch(f'/api/v1/customers/{customer_id}',json=data)
        logger.info(f"rawResp: {response.data}")
        self.assertEqual(response.status_code, 200)
        respData = response.get_json()
        self.assertEqual(respData["data"]['name'], data['name'])

        # delete it
        response = self.client.delete(f'/api/v1/customers/{customer_id}')
        logger.info(f"rawResp: {response.data}")
        self.assertEqual(response.status_code, 200)




        
