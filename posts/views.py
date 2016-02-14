from django.shortcuts import render, get_object_or_404

from .models import Post


def index(request):
    latest_post_list = Post.objects.order_by('pub_date')[:5]
    context = {
        'latest_post_list': latest_post_list
    }
    return render(request, 'posts/index.html', context)

######Copied from django tut1.8, using them as examples
def detail(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    return render(request, 'posts/detail.html', {'post': post})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
########################################################
