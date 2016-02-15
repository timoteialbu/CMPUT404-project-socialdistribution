from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse ### delete me! should be using render
from django.utils import timezone

from .models import Post
from .forms import PostForm

def index(request):
    latest_post_list = Post.objects.order_by('pub_date')[:5]
    context = {
        'latest_post_list': latest_post_list
    }
    return render(request, 'posts/index.html', context)

def createPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/createPost.html', {'form': form})

def publish(request):
    return HttpResponse(request)


######Copied from django tut1.8, using them as examples
def detail(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    return render(request, 'posts/detail.html', {'post': post})

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
########################################################
