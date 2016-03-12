from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

import urllib2
#import unittest
import json

BASEURL = "http://127.0.0.1:8000/api"
factory = APIRequestFactory()
client = APIClient()

class DBTests(TestCase):
    def setUp(self):
        user   = User.objects.create()
        author = Author.objects.create(user=user, displayName="stephen")
        post   = Post.objects.create(author=author, title="cool post", content="cool content")

class TestYourWebserver(TestCase):

    def fill_json_test(self):
        template=json.dumps({
            'title': 'STRING',
            'source': 'localhost',
            'origin': '',
            'description': '',
            'contentType': null,
            'content': '',
            'visibility': null
        })
        return template

    def setUp(self,baseurl=BASEURL):
        """do nothing"""
        self.baseurl = baseurl

    def test_user_post_list(self):
        url = reverse('/author/posts')
        data = {"title": "test",
        "source": "any",
        "origin": "any",
        "description": "none",
        "contentType": "text/json",
        "content": "IMPORTANT STUFF HERE",
        "visibility": null}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(Account.objects.count(), 1)
        #self.assertEqual(Account.objects.get().name, 'DabApps')
        #request = factory.post(url, fill_json_test(),format='json');
        #self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        #self.assertTrue( req.info().gettype() == "text/css", ("Bad mimetype for css! %s" % req.info().gettype()))

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

        '''

        '''

    def test_user_list(self):
        #TODO

    def test_user_detail(self):
        #TODO


    def test_author_post(self):
        '''
        As an author I want to make posts.
        '''


if __name__ == '__main__':
    unittest.main()
