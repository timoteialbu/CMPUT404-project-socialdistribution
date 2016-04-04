from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User # added for friendship
from friendship.models import Friend, Follow, FriendshipRequest
from api.models import *
from .forms import PostForm, UploadImgForm, AddFriendForm, UnFriendUserForm, FriendRequestForm, CommentForm, \
    UserProfile, PostEditForm
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpResponseRedirect
from api.serializers import PostSerializer
from rest_framework.response import Response
from django.template import loader
from django.template import RequestContext
import requests
import base64
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from api.serializers import *
import json
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# not a view can be moved elsewhere
#####################################################
def handle_uploaded_file(f):
        with open('some/file/name.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

#================================================================
# DEBUGGER
def do_debug(debug=True, message="--DEBUG--"):
    if debug:
        print message
#================================================================


#================================================================
#---------------------------- Friends ---------------------------

def try_add_friend(user, friend):
        try:
            friend_id = int(User.objects.get(username=friend).id)
        except Exception:
            return "Not a valid user, please try again."
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
            Friend.objects.add_friend(user, friend)
            msg += " and waiting for them to accept your request."
        except Exception:
            msg += " and already waiting for a response to your request"
        return msg

def add_friend(request, context):
        addform_valid = context['addform'].is_valid(),
        if addform_valid:
            friend = context['addform'].cleaned_data['user_choice_field']
            context['addfriend'] = friend
            if friend is not None:
                context['add_msg'] = try_add_friend(request.user, friend)
        elif not addform_valid:
            context['add_msg'] = "Invalid input"
            context['addform'] = AddFriendForm()

#----------------------------------------------------------------
def friend_requests(request, context, users):
        requests_valid = context['friendrequestform'].is_valid(),
        if requests_valid:
            for user in users:
                req_id = FriendshipRequest.objects.get(to_user=request.user,from_user=User.objects.get(username=user))
                if request.POST[user] == "A":
                    req_id.accept()
                elif request.POST[user] == "R":
                    req_id.reject()
                    try_remove_friend(request.user, user)

            #friend = context['friendrequestform'].cleaned_data['user_choice_field']
            #context['addfriend'] = friend

#----------------------------------------------------------------
def try_remove_friend(user, friend):
        try:
            friend_name = User.objects.get(username=friend)
            friend_id = int(User.objects.get(username=friend).id)
        except Exception:
            return "Not a valid user, please try again."
        msg = ""
        if Follow.objects.remove_follower(user, friend_name):
            msg += "You are no longer following %s" % friend
        else:
            msg += "You are not following %s, so you can't unfollow them." % friend
        if Friend.objects.remove_friend(friend_id, user):
            msg += " You are no longer friends with %s" % friend
        else:
            msg += " You were never friends with %s, I'm sorry :(" % friend
        return msg

def remove_friend(request, context):
        unfrienduserform_valid = context['unfrienduserform'].is_valid()
        if unfrienduserform_valid:
            friend = context['unfrienduserform'].cleaned_data['username']
            friend = friend.strip()
            if str(friend) is not '':
                context['unfriend_msg'] = try_remove_friend(
                    request.user,
                    friend
                )
        elif not unfrienduserform_valid:
            context['unfriend_msg'] = "Invalid input."
            context['unfrienduserform'] = UnFriendUserForm

#----------------------------------------------------------------
def friend_mgmt(request):
    users = list(map(lambda x:
                     str(x.from_user),
                     Friend.objects.unread_requests(request.user)))
    all_friends = Friend.objects.friends(request.user)

    context = {
        'friendrequestform': FriendRequestForm(names=users),
        'all_friends': all_friends
    }

    if request.method == "POST":
        form = PostForm(request.POST)
        context.update({
            'addform': AddFriendForm(request.POST),
            'unfrienduserform': UnFriendUserForm(request.POST),
        })
        remove_friend(request, context)
        add_friend(request, context)
        friend_requests(request, context, users)
    else:
        form = PostForm()
        context.update({
            'addform': AddFriendForm(),
            'unfrienduserform': UnFriendUserForm(),
        })

    print ("all_friends:" , all_friends)
    return render(request, 'posts/friend_mgmt.html', context)


#================================================================
#----------------------------- Posts ----------------------------
def visibility_filter(request, sel):
    # Python's version of a Switch-Case:
    # We can return functions, including
    # defaults and empty functions.
    vis = {
        "PUBLIC": lambda: None,
        "PRIVATE": lambda: None,
        "AUTHOR": lambda: None,
        "FRIENDS": lambda: None,
        "FOAF": lambda: None,
        "SERVERONLY": lambda: None,
    }
    function = vis.get(sel, lambda: None)
    return function

def get_posts(request): # Return QuerySet
    # Returns all posts unless the user is anonymous (then only public)
        if request.user.is_anonymous():
            latest_post_list = Post.objects.filter(Q(visibility='PUBLIC'))
        else:
            latest_post_list = Post.objects.all()
            print(latest_post_list)
        return latest_post_list.order_by('-published')

def filter_posts(request, selection):
    # Returns True if the selection can be seen by the current user
        myuser = selection.author.user
        if myuser == request.user:  # REDUNDANT AS HELL
            return True
        elif selection.visibility == 'FOAF':
            for friend in Friend.objects.friends(request.user):
                friend_list = Friend.objects.friends(friend)
                if (request.user in friend_list):
                    return True
            return False
        elif (
                (selection.visibility == 'AUTHOR' and selection.privateAuthor != request.user)
            or  (selection.visibility == 'FRIENDS' and myusernot in all_friends)
            or  (selection.visibility == 'PRIVATE' and myuser!= request.user)
            or  (selection.visibility == 'SERVERONLY')
            ):
                return False
        else:
            return True

def get_post_detail(request, id):
        # returns a QuerySet
        post_Q = Post.objects.filter(id=id)
        comment = None
        remote = False
        if not post_Q:
            post = get_remote(request, '/posts/' + id + '/')
            comments = post['comments']
            remote = True
        else:
            post = post_Q.values()[0]
            comments = Comment.objects.select_related().filter(post=id)
        if request.method == "POST":
            # Hackyyy OMG
            if not remote:
                form = PostForm(request.POST, instance=post_Q[0])
            else:
                form = PostForm

            cform = CommentForm(request.POST)
            postEditForm = PostEditForm(request.POST)

            if postEditForm.is_valid() and postEditForm.changed_data.__len__() > 0:
                post1 = Post.objects.get(id=id)
                post1.title = postEditForm.cleaned_data["title"]
                post1.content = postEditForm.cleaned_data["content"]
                post1.save()
                return redirect('posts:detail', id=id)
            if not remote and form.is_valid():
                post = form.save(commit=False)
                post.author = Author.objects.get(user=request.user)
                post.published_date = timezone.now()
                post.save()
                # the "id" part must be the same as the P<"id" in url.py
                # return redirect('posts:detail', id=post.pk)
            elif cform.is_valid():
                if not remote:
                    comment = cform.save(commit=False)
                    comment.published = timezone.now()
                    comment.author = Author.objects.get(user=request.user)
                    comment.post = post_Q[0]
                    comment.save()
                else:
                    ext = "/posts/" + str(id) + "/comments"
                    payload = {
                        "comment": request.POST['comment'],
                        "contentType": request.POST['contentType'],
                    }
                    post_remote(request, ext, payload)
        else:
            form = PostForm(initial={'content': post['content']})
            cform = CommentForm()
            postEditForm = PostEditForm()
            post1 = Post.objects.get(id=id)
            postEditForm.fields["title"] = post1.title
            postEditForm.fields["content"] = post1.content
            postEditForm.fields["postId"] = post1.id

        isAuthenticated = request.user.is_authenticated()
        isAuthor = False
        if isAuthenticated and not remote:
            isAuthor = Author.objects.get(user=request.user).user == post_Q[0].author.user
        return render(request, 'posts/detail.html',
                    {
                        'post': post,
                        'comments': comments,
                        'form': form,
                        'cform': cform,
                        'isAuthenticated': isAuthenticated,
                        'isAuthor': isAuthor,
                        'postEditForm': postEditForm
                    })

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get(user=request.user)
            post.published = timezone.now()
            post.save()
            # future ref make to add the namespace ie "posts"
            return redirect('posts:detail', id=post.pk)
    return None

def delete_post(request, id):
        post_list = get_posts(request)
        if request.method == 'POST':
            for post in post_list:
                if str(post.id) == str(id):
                    post.delete()
            return redirect('posts:index')
        return render(request, 'posts/index.html')

def post_mgmt(request):
        latest_post_list = get_posts(request).filter(
            Q(author=Author.objects.get(user=request.user)))
        if request.method == 'POST':
            values = request.POST.getlist('id')
            for post in latest_post_list:
                for id in values:
                    if str(id) == str(post.id):
                        post.delete()

            return redirect('posts:post_mgmt')
        context = {
            'can_add_psot': False,
            'latest_post_list': latest_post_list
        }
        return render(request, 'posts/post_mgmt.html', context)

#----------------------------------------------------------------
# GITHUB
def get_github_posts(request):
    select = Author.objects.get(user=request.user)
    #user = "aaclark"
    user = str(select.github)
    github_posts = list()   # fallback
    if(user!=""):
        url = "https://api.github.com/users/"+user+"/events/public"
        headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/vnd.github.v3+json'
        }
        activity_unparsed=list()
        try:
            activity = requests.get(url, headers=headers)
            print("GITHUB CONNECTED")
        except:
            print("GITHUB API ERROR")

        print(activity) # response 200
    return github_posts

#----------------------------------------------------------------
def get_imgs(request):  # Return QuerySet
        do_debug(request.user)
        return Image.objects.order_by('-published')[:5]

def create_img(request):
    if request.method == 'POST':
        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.author = Author.objects.get(user=request.user)
            img.published = timezone.now()
            img.save()
            return redirect('posts:index')
    else:
        form = UploadImgForm()
    return render(request, 'posts/edit_img.html', {'form': form})

def delete_img(request, id):
        post_list = get_posts(request)
        if request.method == 'POST':
            for post in post_list:
                if str(post.id) == str(id):
                    post.delete()
            return redirect('posts:index')
        return render(request, 'posts/index.html')

#----------------------------------------------------------------
def get_profile(request):
        if request.method == "POST":
            # This request returns 2 dictionaries. The first one is to update the profile,
            # the second one updates a particular post
            formProfile = UserProfile(request.POST)
            formPost = PostEditForm(request.POST)
            if formProfile.is_valid() and formProfile.changed_data.__len__() > 0:
                author = Author.objects.get(user=request.user)
                author.displayName = formProfile.cleaned_data["displayname"]
                author.host = formProfile.cleaned_data["host"]
                author.url = formProfile.cleaned_data["url"]
                author.github = formProfile.cleaned_data["github"]
                author.save()

            if formPost.is_valid() and formPost.changed_data.__len__() > 0:
                post = Post.objects.get(id=formPost.cleaned_data["postId"])
                post.title = formPost.cleaned_data["title"]
                post.content = formPost.cleaned_data["content"]
                post.save()

            return redirect('posts:update_profile')
        else:
            formPost = PostEditForm()
            formProfile = UserProfile()

            latest_post_list = Post.objects.filter(
                Q(author=Author.objects.get(user=request.user)))
            latest_img_list = Image.objects.order_by('-published')[:5]
            author = Author.objects.get(user=request.user)

            formProfile.fields["username"] = request.user.username
            formProfile.fields["displayname"] = author.displayName
            formProfile.fields["host"] = author.host
            formProfile.fields["url"] = author.url
            formProfile.fields["github"] = author.github
            formProfile.fields["id"] = author.id

            context = {
                'latest_image_list': latest_img_list,
                'latest_post_list': latest_post_list,
                'formPost': formPost,
                'formProfile': formProfile,
            }
            return render(request, 'posts/profile.html', context)


#----------------------------------------------------------------

def get_nodes(request):
        nodes_list = Node.objects.all()
        context = {'nodes_list': nodes_list}
        return render(request, 'posts/nodes.html', context)

#----------------------------------------------------------------

def get_remote(request, ext):
        nodes = Node.objects.all()
        r = list()
        for node in nodes:
            url = node.location + ext
            authToken = node.auth_token
            if(authToken == None):
                author = Author.objects.get(user=request.user)
                authStr = str(author.id)+"@team5:team5"
                authToken = "Basic " + str(base64.b64encode(authStr))
            headers = {
                    'Authorization': authToken,
                    'Content-Type': 'application/json',
            }
            do_debug(authToken)
            try:
                r = r + requests.get(url, headers=headers).json()['posts']
            except:
                try:
                    r = r + requests.get(url, headers=headers).json()['results']
                except:
                    do_debug("Unkown API Format!")
                    do_debug(r)
        do_debug(r)
        return r


def post_remote(request, ext, payload):
        nodes = Node.objects.all()
        for node in nodes:
            url = node.location + ext
            authToken = node.auth_token
            if(authToken == None):
                author = Author.objects.get(user=request.user)
                authStr = str(author.id)+"@team5:team5"
                authToken = "Basic " + str(base64.b64encode(authStr))
            headers = {
                    'Authorization': authToken,
                    'Content-Type': 'application/json',
            }
            do_debug ("url" + url)
            r = requests.post(url, headers=headers, json=payload)
        return r.status_code

#----------------------------------------------------------------
def process_form(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                post = Post()
                post.author = Author.objects.get(user=request.user)
                post.title = form.cleaned_data["title"]
                post.content = form.cleaned_data["content"]
                post.contentType = form.cleaned_data["contentType"]
                post.visibility = form.cleaned_data["visibility"]
                test = form.cleaned_data["privateAuthor"]
                do_debug( test + "<---------------- test")
                post.privateAuthor = User.objects.all().filter(id=test.id)
                do_debug (User.objects.all().filter(id=test.id) + "<---------------- after filter")
                do_debug (post.privateAuthor + "<----------------------- post.privateAuthor when created")
                post.save()
                return redirect('posts:index')
            except:
                return 400
    return None # BAD DEFAULT

#----------------------------------------------------------------
# prob should change this to a form view
def index(request):

        remote_posts = list()
        github_posts = list()
        latest_post_list = list()
        latest_img_list = list()

        try:
            latest_post_list = list(get_posts(request))
        except:
            pass

        try:
            remote_posts = list(get_remote(request, '/posts/')['posts'])
        except:
            pass

        try:
            github_posts = list(get_github_posts(request))
        except:
            pass

        try:
            latest_img_list = list(get_imgs(request))
        except:
            pass


    # Fallback on empty form
    # THIS SHOULDN'T EVEN BE HERE
        form = PostForm()
        process_form(request) # Handles properly

        if not (request.user.is_anonymous()):
            my_posts, other_posts = [], []

            # Splits into two lists based on authorship and cantidacy
            for x in latest_post_list:
                if (x.author.user == request.user):
                    my_posts.append(x)
                elif filter_posts(request, x):
                    other_posts.append(x)

            latest_post_list = my_posts + other_posts

        comments_dict = {}
        for p in latest_post_list:
            comments = Comment.objects.filter(post=p.id)
            comments_dict[p.id] = comments

        grouped_list = latest_post_list + remote_posts + github_posts

        context = {
            'latest_image_list': latest_img_list,
            'latest_post_list': grouped_list,
            'form': form,
            'comments_dict': comments_dict,
            'can_add_psot': True
        }
        return render(request, 'posts/index.html', context)
