from api.models import *
from api.serializers import *
from api.models import Author
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
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
def friend_request(request):
        return None
