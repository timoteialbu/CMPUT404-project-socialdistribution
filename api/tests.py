from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

import urllib2
import unittest

BASEURL = "http://127.0.0.1:8000/api"
factory = APIRequestFactory()
client = APIClient()

class TestYourWebserver(unittest.TestCase):
    
    def setUp(self,baseurl=BASEURL):
        """do nothing"""
        self.baseurl = baseurl

    def test_user_post_list(self):
        url = self.baseurl + "/author/posts"
        req = urllib2.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        self.assertTrue( req.info().gettype() == "text/css", ("Bad mimetype for css! %s" % req.info().gettype()))

    def test_post_list(self):
        url = self.baseurl + "/posts"
        req = urllib2.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")

    def test_author_post_list(self):
        url = self.baseurl + "/author/" + authorID + "posts"
        req = urllib2.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!") 
   
    def test_post_detail(self):
        url = self.baseurl + "/post/" + postID
        req = urllib2.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")  

    def test_user_list(self):
        #TODO

    def test_user_detail(self):
        #TODO
    
if __name__ == '__main__':
    unittest.main()
