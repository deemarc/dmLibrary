import requests
import json

from dmLibrary.api.v1 import resources

class GoogleBook(object):

    def __init__(self,timeout=10):
        self.base_url = "https://www.googleapis.com/books/v1"
        self.timeout = 10

    def getPageCount(self,isbn):
        url =  self.base_url + f"/volumes?q=isbn:{isbn}"
        response = requests.get(url)
        if response.status_code != 200:
            return -1
        data = response.json()
        if data['totalItems'] != 1:
            return -1
        volumeInfo = data['items'][0].get("volumeInfo",None)
        if not volumeInfo:
            return -1
        
        pageCount = volumeInfo.get("pageCount",None)
        if not pageCount:
            return -1
            
        return pageCount

