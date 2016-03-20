from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from api.models import *
import urllib2
import unittest
import json


BASEURL = "http://127.0.0.1:8000/api"

# factory generates request instances
factory = APIRequestFactory()
# client acts as a dummy web browser
client = APIClient()


#===============================================================================
#============================= ABSTRACT TEST CLASSES ===========================
#===============================================================================

class TestDatabase(TestCase):
    def setup(self):
        user   = User.objects.create()
        author = Author.objects.create(user=user, displayName="stephen")
        post   = Post.objects.create(author=author, title="cool post", content="cool content")

class TestGenericUsecase(TestCase):
    """GENERIC"""
    def setup(self,baseurl=BASEURL):
        self.baseurl = baseurl
    def generic_json(self):
        """{Returns Generic JSON}"""
        template=json.dumps({
            "title": "LOREM IPSUM",
            "source": "any",
            "origin": "any",
            "description": "none",
            "contentType": "text/json",
            "content": "FILLER CONTENT",
            "visibility": None})
        return template
    def generic_get(self, target='/', expected_code=200):
        """{Sends generic (GET) request to target or webroot}"""
        url = (target)
        response = self.factory.get(url)
        self.assertEqual(response.status_code, expected_code)
        #self.assertEqual(Account.objects.count(), 1)
        #self.assertEqual(Account.objects.get().name, 'DabApps')
        #request = factory.post(url, fill_json_test(),format='json');
        #self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        #self.assertTrue( req.info().gettype() == "text/css", ("Bad mimetype for css! %s" % req.info().gettype()))

    def generic_post(self, target='/', data="TEST", expected_code=202):
        """{Sends generic (POST) request with JSON to target or webroot}"""
        url = (target)
        response = self.factory.post(url, data, format='json')
        self.assertEqual(response.status_code, expected_code)
        #self.assertEqual(Account.objects.count(), 1)
        #self.assertEqual(Account.objects.get().name, 'DabApps')
        #request = factory.post(url, fill_json_test(),format='json');
        #self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        #self.assertTrue( req.info().gettype() == "text/css", ("Bad mimetype for css! %s" % req.info().gettype()))



#===============================================================================
#============================ CONCRETE TEST CLASSES ============================
#===============================================================================

class TestContentCreation(TestCase):
    """CONTENT CREATION"""
    def setup(self,baseurl=BASEURL):
        self.baseurl = baseurl
    def test_author_make_post(self):    # TODO Create and view own
        """- As an author I want to make posts."""
        url = ('/author/posts')
        data = {"title": "Author Posts",
        "source": "any",
        "origin": "any",
        "description": "none",
        "contentType": "text/json",
        "content": "IMPORTANT STUFF HERE",
        "visibility": None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        #self.assertEqual(Account.objects.count(), 1)
        #self.assertEqual(Account.objects.get().name, 'DabApps')
        #request = factory.post(url, fill_json_test(),format='json');
        #self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        #self.assertTrue( req.info().gettype() == "text/css", ("Bad mimetype for css! %s" % req.info().gettype()))
    def test_author_format_post(self):
        """- As an author, posts I make can be in simple plain text
        - As an author, posts I make can be in markdown (commonMark is good)"""
    def test_author_image_post(self):
        """- As an author, posts I create can link to images."""
    def test_author_remove_post(self):
        """- As an author, I want to delete my own posts."""
    def test_author_make_comment(self):
        """- As an author, I want to comment on posts that I can access"""

class TestContentPrivacy(TestCase):
    """CONTENT PRIVACY"""
    def setup(self,baseurl=BASEURL):
        self.baseurl = baseurl
    def test_user_view_list(self):
        """[Should verify that registered users can view lists of posts]"""
        url = "/posts"
        response = self.client.get(url)
        self.assertTrue( response.status_code  == 200 )
    def test_user_view_post(self, postID=1):
        """[Should verify that registered users can view single posts]"""
        url = "/post/" + str(postID)
        response = self.client.get(url)
        self.assertTrue( response.status_code  == 200 )
    def test_anon_view_list(self):
        """[Should verify that anonymous users view restricted lists of posts]"""
        url = "/posts"
        response = self.client.get(url)
        self.assertTrue( response.status_code  == 200 )
    def test_anon_view_post(self, postID=1):
        """[Should verify that anonymous users view restricted posts]"""
        url = "/post/" + str(postID)
        response = self.client.get(url)
        self.assertTrue( response.status_code  == 200 )

class TestUserPrivacy(TestCase):
    """USER PRIVACY"""
    def setup(self,baseurl=BASEURL):
        self.baseurl = baseurl
    def test_privacy_self(self):
        """- As an author, posts I create be private to me"""
    def test_privacy_other(self):
        """- As an author, posts I create be private to another author"""
    def test_privacy_friends(self):
        """- As an author, posts I create be private to my friends"""
    def test_privacy_acquaint(self):
        """- As an author, posts I create be private to friends of friends"""
    def test_privacy_locals(self):
        """- As an author, posts I create be private to only friends on my host"""
    def test_privacy_public(self):
        """- As an author, posts I create can be public"""
    def test_auth_view(self):
        """- As an author, I want to feel safe about sharing images and posts
        with my friends -- images should not publicly accessible without authentication."""
    def test_auth_edit(self):
        """- As an author, other authors cannot modify my data"""
    def test_browse_public(self):
        """- As an author I should be able to browse the public posts of everyone"""
    def test_browse_status(self):
        """- As an author I should be able to browse the posts of others depending on my status"""


class TestUserProfiles(TestCase):
    """USER PROFILES"""
    def setup(self,baseurl=BASEURL):
        self.baseurl = baseurl
    def test_profile_consist(self):
        """- As an author, I want a consistent id per server"""
    def test_profile_friends(self):
        """- As an author, my server will know about my friends"""
    #def test_profile_browse(self):
    #def test_profile_edit(self):

    ''' # TODO Fill out these stubs
    class TestUserConnections(TestCase):
    class TestGithub(TestCase):
    class TestBrowser(TestCase):
    class TestContentControl(TestCase):
    class TestUserControl(TestCase):
    class TestNetworkControl(TestCase):
    '''

    def purposeless_filler(self):
        #'''    # USER STORIES FOR TESTS
        #======================================
        # Content Creation
        """- As an author I want to make posts."""
        """- As an author, I want to delete my own posts."""
        """- As an author, I want to comment on posts that I can access"""

        # Post formatting
        """- As an author, posts I make can be in simple plain text"""
        """- As an author, posts I make can be in markdown (commonMark is good)"""
        """- As an author, posts I create can link to images."""

        # User privacy
        """- As an author, posts I create be private to me"""
        """- As an author, posts I create be private to another author"""
        """- As an author, posts I create be private to my friends"""
        """- As an author, posts I create be private to friends of friends"""
        """- As an author, posts I create be private to only friends on my host"""
        """- As an author, posts I create can be public"""
        """- As an author, I want to feel safe about sharing images and posts
        with my friends -- images should not publicly accessible without authentication."""
        """- As an author, other authors cannot modify my data"""
        """- As an author I should be able to browse the public posts of everyone"""
        """- As an author I should be able to browse the posts of others depending on my status"""

        # User Profiles
        """- As an author, I want a consistent id per server"""
        """- As an author, my server will know about my friends"""

        #---------------- v TODO v ---------------

        # User Connections
        """- As an author, I want to befriend local authors"""
        """- As an author, I want to befriend remote authors"""
        """- As an author, When I befriend someone it follows them, only when
        the other authors befriends me do I count as a real friend."""
        """- As an author, I want to know if I have friend requests."""
        """- As an author, I want to un-befriend local and remote authors"""


        # Github API
        """- As an author, I want to pull in my github activity to my "stream"""
        """- As an author, I want to post posts to my "stream"""

        # Browser Compatibility
        """- As an author, I want to be able to use my web-browser to manage my profile"""
        """- As an author, I want to be able to use my web-browser to manage/author my posts"""
        """- As a server admin, I want a restful interface for most operations"""


        # Admin Content Control
        """- As a server admin, images can be hosted on my server."""
        """- As a server admin, I want to host multiple authors on my server"""
        """- As a server admin, I want to share or not share posts with users
        on other servers."""
        """- As a server admin, I want to share or not share images with users
        on other servers."""

        # Admin User Control
        """- As a server admin, I want to be able add, modify, and remove authors."""
        """- As a server admin, I want to be able allow users to sign up but
        require my OK to finally be on my server"""
        """- As a server admin, I don't want to do heavy setup to get the
        posts of my author's friends."""

        # Admin Networking Control
        """- As a server admin, I want to be able to add nodes to share with"""
        """- As a server admin, I want to be able to remove nodes and stop
        sharing with them."""
        """- As a server admin, I can limit nodes connecting to me via
        authentication."""
        """- As a server admin, node to node connections can be authenticated
        with HTTP Basic Auth"""
        """- As a server admin, I can disable the node to node interfaces for
        connections that are not authenticated!"""
        #'''




if __name__ == '__main__':
    unittest.main()
