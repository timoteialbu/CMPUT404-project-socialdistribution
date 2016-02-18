from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from .models import Post, Image, Friend
from .forms import PostForm, UploadImgForm, FriendForm


# not a view can be moved elsewhere
#####################################################
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def get_posts(request):
    latest_post_list = Post.objects.filter(
        Q(privacy='PU') |
        Q(author=request.user))# |
        # Q(author__accepted_friends__users_friends=request.user) |
        # Q(author__friend_requests__friend_with=request.user)
        #)
    return latest_post_list
#####################################################


def create_friend(request):
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            friend = form.save(commit=False)
            friend.users_friends = request.user
            friend.save()
            return redirect('posts:index')
    else:
        form = FriendForm()
    return render(request, 'posts/edit_img.html', {'form': form})






def index(request):
    latest_post_list = get_posts(request)
    latest_img_list = Image.objects.order_by('-pub_date')[:5]
    context = {
        'latest_image_list': latest_img_list,
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
            # future ref make to add the namespace ie "posts"
            return redirect('posts:detail', post_id=post.pk)
    else:
        form = PostForm()
    # this is forsure broken but doesnt get reached
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
            # the "post_id" part must be the same as the P<"post_id" in url.py
            return redirect('posts:detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form})


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/detail.html', {'post': post})


def create_img(request):
    if request.method == 'POST':
        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.author = request.user
            img.pub_date = timezone.now()
            img.save()
            return redirect('posts:index')
    else:
        form = UploadImgForm()
    # this is prob broken but doesnt get reached
    return render(request, 'posts/edit_img.html', {'form': form})


