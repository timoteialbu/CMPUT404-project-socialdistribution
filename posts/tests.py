from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from api.models import *
from django.test.utils import setup_test_environment

setup_test_environment()


def new_author(username="john", email="dd@dsd.ca", password="123454"):
	if User.objects.filter(username=username).exists():
		user = User.objects.get(username=username)
		return Author.objects.get(user=user)
	user = User.objects.create_user(username, email, password)
	return Author.objects.get(user=user, )


def create_post(author, content, days, visibility):
	"""
	Creates a post with the given `post_text` published the given
	number of `days` offset to now (negative for questions published
	in the past, positive for post that have yet to be published).
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Post.objects.create(author=author, content=content,
							   published=time, visibility=visibility)


class QuestionViewTests(TestCase):
	def test_index_view_with_no_posts(self):
		"""
		If no post exist, an appropriate message should be displayed.
		"""
		response = self.client.get('/posts')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No posts are available!")
		self.assertQuerysetEqual(response.context['latest_post_list'], [])

	def test_index_view_with_a_past_post(self):
		"""
		Posts with a pub_date in the past should be displayed on the
		index page.
		"""

		post_text = "Past post."
		days = -30
		author = new_author()
		create_post(author, post_text, days, "PU")
		response = self.client.get('/posts')
		self.assertQuerysetEqual(
			response.context['latest_post_list'],
			['<Post: Past post.>']
		)

# def test_index_view_with_a_future_post(self):
#         """
#         Posts with a pub_date in the future should not be displayed on
#         the index page.
#         """
#         post_text="Past post."
#         days=30
#         create_post(new_user(), post_text, days, "PU")
#         response = self.client.get(reverse('posts:index'))
#         print response
#         self.assertContains(response, "No posts are available!",
#                             status_code=200)
#         self.assertQuerysetEqual(response.context['latest_post_list'], [])

#    def test_index_view_with_future_post_and_past_post(self):
#         """
#         Even if both past and future posts exist, only past posts
#         should be displayed.
#         """
#         post_text_past="Past post."
#         post_text_future = "Future post."
#         past_days = -30
#         future_days = 30
#         create_post(new_user(), post_text_past, past_days, "PU")
#         create_post(new_user(), post_text_future, future_days, "PU")
#         response = self.client.get(reverse('posts:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_post_list'],
#             ['<Post: Past post.>']
#         )

#    def test_index_view_with_two_past_posts(self):
#         """
#         The posts index page may display multiple posts.
#         """
#         post_text_1 = "Past post 1."
#         post_text_2 = "Past post 2."
#         days_1= -30
#         days_2= -5
#         create_post(new_user(), post_text_1, days_1, "PU")
#         create_post(new_user(), post_text_2, days_2, "PU")
#         response = self.client.get(reverse('posts:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_post_list'],
#             ['<Post: Past post 2.>', '<Post: Past post 1.>']
#         )
