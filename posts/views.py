from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User  # added for friendship
from friendship.models import Friend, Follow, FriendshipRequest
from api.models import *
from .forms import PostForm, UploadImgForm, AddFriendForm, FriendRequestForm, CommentForm, \
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


# ================================================================
# DEBUGGER
def do_debug(debug=True, message="--DEBUG--"):
	if debug:
		print message


# ================================================================


# ================================================================
# ---------------------------- Friends ---------------------------

def try_add_friend(user, friend):
	msg = ""
	try:
		friend_object = User.objects.get(username=friend)
	except Exception:
		return "Not a valid user, please try again."
	try:
		Follow.objects.add_follower(user, friend_object)
		msg += "You are now following %s" % friend
	except Exception:
		msg += "You are already following %s" % friend
	try:
		Friend.objects.add_friend(user, friend_object)
		msg += " and waiting for them to accept your request."
	except Exception:
		msg += " and already waiting for a response to your request"
	return msg


def add_friend(request, context):
	addform_valid = context['addform'].is_valid(),
	if addform_valid:
		friend = context['addform'].cleaned_data['add_username']
		friend = friend.strip()
		# context['addfriend'] = friend
		if friend is not '':
			context['add_msg'] = try_add_friend(request.user, friend)
	elif not addform_valid:
		context['add_msg'] = "Invalid input"
		context['addform'] = AddFriendForm()


# ----------------------------------------------------------------
def try_remove_friend(user, friend):
	try:
		friend_name = User.objects.get(username=friend)
	except Exception:
		return "Not a valid user, please try again."
	msg = ""
	if Follow.objects.remove_follower(user, friend_name):
		msg += "You are no longer following %s" % friend
	else:
		msg += "You are not following %s, so you can't unfollow them." % friend
	if Friend.objects.remove_friend(friend_name, user):
		msg += " You are no longer friends with %s" % friend
	else:
		msg += " You were never friends with %s, I'm sorry :(" % friend
	return msg


def remove_friend(request, context):
	friendList = request.POST.getlist('remove')
	context['unfriend_msg'] = []
	for friend in friendList:
		context['unfriend_msg'].append(str(try_remove_friend(request.user, friend)))


# ----------------------------------------------------------------
def friend_requests(request, context, users):
	requests_valid = context['friendrequestform'].is_valid(),
	if requests_valid:
		for user in users:
			userId = User.objects.get(username=user)
			req_id = FriendshipRequest.objects.get(to_user=request.user, from_user=userId)
			if request.POST[user] == "A":
				req_id.accept()
				Follow.objects.add_follower(request.user, userId)
			elif request.POST[user] == "R":
				req_id.reject()
				Friend.objects.remove_friend(userId, request.user)
				try_remove_friend(request.user, user)


# ----------------------------------------------------------------


def friend_mgmt(request):
    usersRequest = list(map(lambda x:
                     str(x.from_user),
                     Friend.objects.unrejected_requests(user=request.user)))
    context = {
        'friendrequestform': FriendRequestForm(names=usersRequest),
    }

    if request.method == "POST":
        context.update({
            'addform': AddFriendForm(request.POST),
            'unfriendlist': Friend.objects.friends(request.user),
        })
        if 'add_sub' in request.POST:
            add_friend(request, context)
        elif 'remove_sub' in request.POST:
            remove_friend(request, context)
        elif 'request_sub' in request.POST:
            friend_requests(request, context, usersRequest)
    else:
        context.update({
            'addform': AddFriendForm(),
            'unfriendlist': Friend.objects.friends(request.user),
        })
    return render(request, 'posts/friend_mgmt.html', context)

#================================================================
#----------------------------- Posts ----------------------------

def visibility_filter(request, label):
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
	function = vis.get(label, lambda: None)
	return function


def filter_posts(request, selection):
    # Returns True if the selection can be seen by the current user
        myuser = selection.author.user
        all_friends = Friend.objects.friends(request.user)

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
            or  (selection.visibility == 'FRIENDS' and myuser not in all_friends)
            or  (selection.visibility == 'PRIVATE' and myuser!= request.user)
            ):
                return False
        elif (selection.visibility == 'SERVERONLY'):
            if (Author.objects.get(user=request.user).host != selection.author.host) or myuser not in all_friends:
                return False
            else:
                return True
        else:
            return True


def get_posts(request):  # Return QuerySet
	# Returns all posts unless the user is anonymous (then only public)
	if request.user.is_anonymous():
		latest_post_list = Post.objects.filter(Q(visibility='PUBLIC'))
	else:
		latest_post_list = Post.objects.all()
	return latest_post_list.order_by('-published')


def get_post_detail(request, id):
        # returns a QuerySet
        post_Q = Post.objects.filter(id=id)
        comment = None
        remote = False
        if not post_Q:
            if request.method == "POST":
                    ext = "/posts/" + id + "/comments"
                    authID = request.user.id
                    payload = {
                        "author": {
                            "id": authID,
                            "host": "http://murmuring-lowlands-80126.herokuapp.com/api",
                            "displayName": str(authID),
                            "url": "http://murmuring-lowlands-80126.herokuapp.com/api",
                            "github": ""
                        },
                        "comment": request.POST['comment'],
                        "contentType": request.POST['contentType'],
                    }
                    response = comment_remote(request, ext, payload)
            post = get_remote_post_detail(request, '/posts/' + id + '/')
            comments = post['comments']
            remote = True
            cform = CommentForm(request.POST)
            isAuthenticated = request.user.is_authenticated()
            return render(request, 'posts/detail.html',
                        {
                            'post': post,
                            'comments': comments,
                            'remote': remote,
                            'cform': cform,
                            'isAuthenticated': isAuthenticated
                        })
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

#----------------------------------------------------------------
def process_form(request):
	print("TESTING")
	form = PostForm(request.POST)
	if form.is_valid():
		try:
			post = Post()
			post.author = Author.objects.get(user=request.user)
			post.title = form.cleaned_data["title"]
			post.content = form.cleaned_data["content"]
			post.contentType = form.cleaned_data["contentType"]
			post.visibility = form.cleaned_data["visibility"]
			post.privateAuthor = form.cleaned_data["privateAuthor"]
			# print(User.objects.all().filter(id=test.id) + "<---------------- after filter")
			# print(post.privateAuthor + "<----------------------- post.privateAuthor when created")
			post.save()
		except:
			print("PROBLEM PROCESSING FORM")
	return redirect('posts:index')


def create_post(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		print("TESTING CREATE")
		if form.is_valid():
			post = form.save(commit=False)
			post.author = Author.objects.get(user=request.user)
			post.published = timezone.now()
			post.save()
			# future ref make to add the namespace ie "posts"
			return redirect('posts:detail', id=post.pk)
	return render(request, 'posts/post_mgmt.html', context)


def delete_post(request, id):
	post_list = get_posts(request)
	if request.method == 'POST':
		for post in post_list:
			if str(post.id) == str(id):
				post.delete()
		return redirect('posts:index')
	return render(request, 'posts/index.html')


# ----------------------------------------------------------------
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


# ----------------------------------------------------------------
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


# ================================================================
# -------------------------- Github API --------------------------
def get_github_posts(request):
	select = Author.objects.get(user=request.user)
	# user = "aaclark"
	user = str(select.github)
	github_posts = list()  # fallback
	if (user != ""):
		url = "https://api.github.com/users/" + user + "/events/public"
		headers = {
			'Content-Type': 'application/json; charset=utf-8',
			'Accept': 'application/vnd.github.v3+json'
		}
		activity_unparsed = list()
		try:
			activity = requests.get(url, headers=headers)
			print("GITHUB CONNECTED")
		except:
			print("GITHUB API ERROR")

		print(activity)  # response 200
	return github_posts


# ================================================================
# ---------------------------- Profile ---------------------------
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


# ================================================================
# ------------------------- Remote Hosts -------------------------
def get_nodes(request):
	nodes_list = Node.objects.all()
	context = {'nodes_list': nodes_list}
	return render(request, 'posts/nodes.html', context)


#----------------------------------------------------------------
def comment_remote(request, ext, payload):
        nodes = Node.objects.all()
        for node in nodes:
            url = node.location + ext + "/"
            authToken = node.auth_token
            if(authToken == None):
                author = Author.objects.get(user=request.user)
                authStr = str(author.id)+"@team5:team5team5"
                authToken = "Basic " + str(base64.b64encode(authStr))
            headers = {
                    'Authorization': authToken,
                    'Content-Type': 'application/json',
            }
            do_debug(authToken)
            print(payload)
            #payload = JSON.stringify(payload)
            try:
                response = requests.post(url, headers=headers, json=payload)
                print(url)
                print(response.json())
            except:
                print("Error on Remote Comment")
                do_debug("Error on Remote Comment")
                do_debug(response)
        return response
    

def get_remote_posts(request, ext):
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
        print(r)
        return r
def get_remote_post_detail(request, ext):
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
            do_debug(authToken)
            try:
                r = requests.get(url, headers=headers).json()
                if 'id' in r:
                    return r
            except:
                do_debug("Unkown API Format!")
                do_debug(r)
        do_debug(r)
        return None


def post_remote(request, ext, payload):
	nodes = Node.objects.all()
	for node in nodes:
		url = node.location + ext
		authToken = node.auth_token
		if (authToken == None):
			author = Author.objects.get(user=request.user)
			authStr = str(author.id) + "@team5:team5"
			authToken = "Basic " + str(base64.b64encode(authStr))
		headers = {
			'Authorization': authToken,
			'Content-Type': 'application/json',
		}
		do_debug("url" + url)
		r = requests.post(url, headers=headers, json=payload)
	return r.status_code


# ================================================================
# -------------------------- Main Render -------------------------
def index(request):
	remote_posts = list()
	github_posts = list()
	latest_post_list = list()
	latest_img_list = list()

	# Fallback on empty form
	# THIS SHOULDN'T EVEN BE HERE
	form = PostForm()
	if request.method == "POST":
		print("MORE DEBUGGING")
		process_form(request)  # Handles properly
	try:
		latest_post_list = list(get_posts(request))
	except:
		pass

	try:
		latest_img_list = list(get_imgs(request))
	except:
		pass

	try:
		remote_posts = list(get_remote_posts(request, '/posts/'))
	except:
		pass

	try:
		github_posts = list(get_github_posts(request))
	except:
		pass

	if not (request.user.is_anonymous()):
		my_posts, other_posts = [], []

		# Splits into two lists based on authorship and candidacy
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
