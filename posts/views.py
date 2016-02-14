from django.http import HttpResponse
from .models import Post

def index(request):
    latest_post_list = Post.objects.order_by('pub_date')[:5]
    output = ', '.join([p.post_text for p in latest_post_list])
    return HttpResponse(output)


######Copied from django tut1.8, using them as examples
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
########################################################
