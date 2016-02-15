from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse ### delete me! should be using render
from django.utils import timezone

from .models import Post
from .forms import PostForm

def index(request):
    ##set to show only 5
    latest_post_list = Post.objects.order_by('pub_date')[:5]
    context = {
        'latest_post_list': latest_post_list
    }
    return render(request, 'posts/index.html', context)

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            ###future ref make to add the namespace ie "posts"
            return redirect('posts:detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/edit_post.html', {'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            ####the "post_id" part must be the same as the P<"post_id" in url.py
            return redirect('posts:detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form})



def detail(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    return render(request, 'posts/detail.html', {'post': post})

