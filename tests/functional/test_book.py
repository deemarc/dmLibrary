import unittest
from dmLibrary import create_app
from dmLibrary.external.googleBook import GoogleBook
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestBookClass(unittest.TestCase):
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

    def test_postBook(self):
        """
        test post new book, try update, and delete it
        """
        
        data = {
            "title":"เรียนรู้วิถีชีวิต ประเพณี พิธีกรรม และความเชื่อแบบบูรณาการ",
            "isbn":"9748846709"
        }
        response = self.client.post('/api/v1/books',json=data)
        logger.info(f"rawResp: {response.data}")
        self.assertEqual(response.status_code, 201)
        respData = response.get_json()
        self.assertEqual(respData["data"]['title'], data['title'])
        self.assertEqual(respData["data"]['isbn'], data['isbn'])
        pageCount = self.gb.getPageCount(data["isbn"])
        self.assertEqual(respData["data"]['pageCount'], 159)
        logger.info(f"respData: {respData}")
        book_id = respData["data"]["id"]

        # try update the title
        data = {
            "title":"test update Book"
        }
        response = self.client.patch(f'/api/v1/books/{book_id}',json=data)
        logger.info(f"rawResp: {response.data}")
        self.assertEqual(response.status_code, 200)
        respData = response.get_json()
        self.assertEqual(respData["data"]['title'], data['title'])
        # delete it
        response = self.client.delete(f'/api/v1/books/{book_id}')
        logger.info(f"rawResp: {response.data}")
        self.assertEqual(response.status_code, 200)




        
