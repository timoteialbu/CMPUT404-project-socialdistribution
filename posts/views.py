from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect ### delete me! should be using render
from django.utils import timezone



from .models import Post, Image
from .forms import PostForm, UploadImgForm

##### not a view can be moved elsewhere
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)







def index(request):
    ##set to show only 5
    latest_post_list = Post.objects.order_by('pub_date')[:5]
    latest_img_list = Image.objects.order_by('-pub_date')[:5]
    print "fuck",latest_img_list,"fuckdddd"
    for image in latest_img_list:
        print image.img
        image = str(image)[7:]
        print image

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
    return render(request, 'posts/edit_img.html', {'form':form})


# def edit_img(request, post_id):
#     img = get_object_or_404(Image, pk=post_id)
#     if request.method == "POST":
#         form = UploadImgForm(request.POST, instance=img)
#         if form.is_valid():
#             img = form.save(commit=False)
#             img.author = request.user
#             img.published_date = timezone.now()
#             post.save()
#             ####the "post_id" part must be the same as the P<"post_id" in url.py
#             return redirect('posts:index', post_id=post.pk)
#     else:
#         form = UploadImgForm(instance=post)
#     return render(request, 'posts/edit_post.html', {'form': form})
