from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User # added for friendship
from friendship.models import Friend, Follow
from .models import Post, Image
from .forms import PostForm, UploadImgForm, AddFriendForm, UnFriendUserForm


# not a view can be moved elsewhere
#####################################################
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def get_posts(request):
    latest_post_list = Post.objects.filter(
        Q(privacy='PU') |
        Q(author=request.user))
    return latest_post_list


# add more logic in here to deal with (waiting for requests/unfolled) state
def try_adding_friend(user, friend):
    msg = ""
    try:
        User.objects.get(username=friend)
    except Exception:
        return "Not a valid user, please try again."
    try:
        Follow.objects.add_follower(user, friend)
        msg += "You are now following %s" % friend
    except Exception:
        msg += "You are already following %s" % friend
    try:
        ##################################################
        # Friend.objects.add_friend(user, friend)
        msg += " and waiting for them to accept your request." % friend
    except Exception:
        msg += " and already waiting for a response to your request"
    return msg


def try_remove_relationship(user, friend):
    try:
        friend_id = int(User.objects.get(username=friend).id)
    except Exception:
        return "Not a valid user, please try again."
    msg = ""
    if Follow.objects.remove_follower(user, friend_id):
        msg += "You are no longer following %s" % friend
    else:
        msg += "You are not following %s, so you can't unfollow them." % friend
    if Friend.objects.remove_friend(friend_id, user):
        msg += " You are no longer friends with %s" % friend
    else:
        msg += " You were never friends with %s, I'm sorry :(" % friend
    return msg
#####################################################


#################DELETE ME JUST FOR REF#####################
def my_view(request):
    # List of this user's friends
    all_friends = Friend.objects.friends(request.user)

    # List all unread friendship requests
    requests = Friend.objects.unread_requests(user=request.user)

    # List all rejected friendship requests
    rejects = Friend.objects.rejected_requests(user=request.user)

    # Count of all rejected friendship requests
    reject_count = Friend.objects.rejected_request_count(user=request.user)

    # List all unrejected friendship requests
    unrejects = Friend.objects.unrejected_requests(user=request.user)

    # Count of all unrejected friendship requests
    unreject_count = Friend.objects.unrejected_request_count(user=request.user)

    # List all sent friendship requests
    sent = Friend.objects.sent_requests(user=request.user)

    # List of this user's followers
    all_followers = Follow.objects.followers(request.user)

    # List of who this user is following
    following = Follow.objects.following(request.user)

    ### Managing friendship relationships

    # Create a friendship request
    other_user = User.objects.get(pk=1)
    new_relationship = Friend.objects.add_friend(request.user, other_user)

    # Can optionally save a message when creating friend requests
    message_relationship = Friend.objects.add_friend(
        from_user=request.user,
        to_user=some_other_user,
        message='Hi, I would like to be your friend',
    )

    # And immediately accept it, normally you would give this option to the user
    new_relationship.accept()

    # Now the users are friends
    Friend.objects.are_friends(request.user, other_user) == True

    # Remove the friendship
    Friend.objects.remove_friend(other_user, request.user)

    # Create request.user follows other_user relationship
    following_created = Follow.objects.add_follower(request.user, other_user)
#######################################################################


def tempFriendDebug(user, friend):
    print "List of this user's friends"
    print Friend.objects.friends(user)
    print " List all unread friendship requests"
    print Friend.objects.unread_requests(user=user)
    print " List all rejected friendship requests"
    print Friend.objects.rejected_requests(user=user)
    print " List all unrejected friendship requests"
    print Friend.objects.unrejected_requests(user=user)
    print " List all sent friendship requests"
    print Friend.objects.sent_requests(user=user)
    print " List of this user's followers"
    print Follow.objects.followers(user)
    print " List of who this user is following"
    print Follow.objects.following(user)


def add_friend(request, context):
    ###############################################################
    unfrienduserform_valid = context['unfrienduserform'].is_valid()
    if unfrienduserform_valid:
        friend = context['unfrienduserform'].cleaned_data['username']
        friend = friend.strip()
        if str(friend) is not '':
            context['unfriend_msg'] = try_remove_relationship(
                request.user,
                friend,
            )
    elif not unfrienduserform_valid:
        context['unfriend_msg'] = "Invalid input."
        context['unfrienduserform'] = UnFriendUserForm
    ###############################################################


def remove_relationship(request, context):
    addform_valid = context['addform'].is_valid(),
    if addform_valid:
        friend = context['addform'].cleaned_data['user_choice_field']
        context['addfriend'] = friend
        if friend is not None:
            context['add_msg'] = try_adding_friend(request.user, friend)
    elif not addform_valid:
        context['add_msg'] = "Invalid input"
        context['addform'] = AddFriendForm()
    ###############################################################


# breaks when add and remove are the same cant find the relationship
def friend_mgnt(request):
    tempFriendDebug(request.user, 'butt')
    if request.method == "POST":
        context = {
            'addform': AddFriendForm(request.POST),
            'unfrienduserform': UnFriendUserForm(request.POST),
        }
        remove_relationship(request, context)
        add_friend(request, context)
        return render(request, 'posts/friend_mgnt.html', context) 
    else:
        addform = AddFriendForm()
        unfollowform = UnFriendUserForm()
    return render(request, 'posts/friend_mgnt.html', {
        'addform': addform,
        'unfrienduserform': unfollowform,
    })


# prob should change this to a form view
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
    return render(request, 'posts/edit_img.html', {'form': form})
