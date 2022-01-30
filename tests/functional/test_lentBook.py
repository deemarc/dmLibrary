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

    def test_lentBook(self):
        """
        test lent book
        """

        #  ===== populate book and customer need for testing ======
        # book 1
        data = {
            "title":"ทายชีวิตคู่ด้วยเลข ๗ ตัว",
            "isbn":"9789740212201"
        }

        response = self.client.post('/api/v1/books',json=data)
        logger.info(f"rawResp: {response.status_code}")
        if not ((response.status_code == 200) or (response.status_code == 201)):
            self.fail("book1 cannot be create")
        respData = response.get_json()
        book1_id = respData["data"]["id"]

        # customerA
        data = {
            "name":"customerA testLastNameA",
            "email":"customerA@gmail.com",
            "mobile":"0881111111"
        }

        response = self.client.post('/api/v1/customers',json=data)
        if not ((response.status_code == 200) or (response.status_code == 201)) :
            self.fail("customerA cannot be create")
        respData = response.get_json()
        customerA_id = respData["data"]["id"]

        # customerB
        data = {
            "name":"customerB testLastNameB",
            "email":"customerB@gmail.com",
            "mobile":"0881111112"
        }
        response = self.client.post('/api/v1/customers',json=data)
        if not ((response.status_code == 200) or (response.status_code == 201)) :
            self.fail("customerB cannot be create")
        respData = response.get_json()
        customerB_id = respData["data"]["id"]


        #check if book1 being lent
        logger.info(f"getting book1 data: /api/v1/books/{book1_id}")
        response = self.client.get(f'/api/v1/books/{book1_id}')
        logger.info(f"rawResp: {response.status_code}")
        if not (response.status_code == 200):
            self.fail("cannot get book1 data")
        respData = response.get_json()
        self.assertEqual(respData["data"]['isLent'], False)
     
        # ==== get history before lent
        response = self.client.get(f'/api/v1/lentHistory?book_id={book1_id}')
        if not (response.status_code == 200):
            self.fail("cannot get lentHistory")
        respData = response.get_json()
        lentCount = len(respData["data"])

        # customerA lent the book
        data ={
            "book_id_list":[book1_id]
        }
        logger.info(f"lenting book: /api/v1/customers/{customerA_id}/lent")
        response = self.client.post(f'/api/v1/customers/{customerA_id}/lent',json=data)
        if not (response.status_code == 200):
            self.fail("customerA cannot lent book1")
        respData = response.get_json()
        customerA_id = respData["data"]["id"]

        #check if book1 being lent
        logger.info(f"getting book1 data: /api/v1/books/{book1_id}")
        response = self.client.get(f'/api/v1/books/{book1_id}')
        logger.info(f"rawResp: {response.status_code}")
        if not (response.status_code == 200):
            self.fail("cannot get book1 data")
        respData = response.get_json()
        self.assertEqual(respData["data"]['isLent'], True)

        # customerB shouldn't be able to lent
        data ={
            "book_id_list":[book1_id]
        }
        response = self.client.post(f'/api/v1/customers/{customerB_id}/lent',json=data)
        if not (response.status_code == 400):
            self.fail("customerA somehow be able to lent the book")


        # customerA return the book
        response = self.client.post(f'/api/v1/customers/{customerA_id}/return',json=data)
        if not (response.status_code == 200):
            self.fail("customerA cannot return the book")
        respData = response.get_json()
        customerA_id = respData["data"]["id"]

        #check if book1 not being lent
        logger.info(f"getting book1 data: /api/v1/books/{book1_id}")
        response = self.client.get(f'/api/v1/books/{book1_id}')
        logger.info(f"rawResp: {response.status_code}")
        if not (response.status_code == 200):
            self.fail("cannot get book1 data")
        respData = response.get_json()
        self.assertEqual(respData["data"]['isLent'], False)

        # ==== check history after lent
        response = self.client.get(f'/api/v1/lentHistory?book_id={book1_id}',json=data)
        if not (response.status_code == 200):
            self.fail("cannot get lentHistory")
        respData = response.get_json()
        lentCountNew = len(respData["data"])
        self.assertEqual(lentCountNew, lentCount+1)






        
