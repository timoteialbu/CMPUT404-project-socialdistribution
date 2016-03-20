from api.models import *
from api.serializers import *
from django.utils import simplejson

def get_posts(user, nodes):
    post_list = []
    for node in nodes:
        url = node.location + '/api/posts'
        r = requests.get(url)
        for post in serializers.deserialize("JSON", r):
            post_list.append(post)
    return post_list
        
        
