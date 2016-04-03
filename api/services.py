from api.serializers import *
from api.models import Author

from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def friend_relationship(request, uuid):
	'''GET returns friends of author_id'''
	# a reponse if friends or not
	# ask a service GET http://service/friends/<authorid>

	if request.method == 'GET':
		# Find the author object with that uuid
		username = Author.objects.get(id=uuid)
		# Get all the friends
		all_friends = Friend.objects.friends(username.user)
		# Get the authors objects version of those friends objects
		all_authors = Author.objects.filter(user__in=all_friends)
		list_return = []
		for i in all_authors:
			list_return.append(i.id)
		response = {
			"query": "friends",
			"authors": list_return
		}
		return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def friends_check(request, friend1_uuid, friend2_uuid):
	"""
	Returns your friend relationship with a certain author
	http://service/friends/(?P<uuid>[^/]+)/(?P<uuid>[^/]+)
	"""
	# Find the author object with that uuid
	username_1 = Author.objects.get(id=friend1_uuid)
	username_2 = Author.objects.get(id=friend2_uuid)
	# Check if friends
	result = Friend.objects.are_friends(username_1.user, username_2.user)

	return Response(
		{
			"query": "friends",
			"authors": [friend1_uuid, friend2_uuid],
			"friends": result
		}
	)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def friend_request(request):
	return None
