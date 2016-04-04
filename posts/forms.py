from django import forms
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, FriendshipRequest
from api.models import Post, Image, Comment
import uuid

# i dont know what meta does ?
class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 1, 'size': 40, 'maxlength': 40}))
    privateAuthor = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 40, 'rows': 1, 'size': 40, 'maxlength': 20, 'placeholder': 'AuthorID (Private to an Author)'}))   
    privateAuthor.label='Private Author'

    class Meta:
        model = Post
        fields = ('title', 'content', 'visibility', 'privateAuthor', 'contentType')


class PostEditForm(forms.Form):
	title = forms.CharField(label='Title', required=False)
	content = forms.CharField(label='Content', required=False)
	postId = forms.UUIDField(label='Id')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'contentType')


class UploadImgForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'img')


class AddFriendForm(forms.Form):
    user_choice_field = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
    )
    fields = ('username',)


class UserProfile(forms.Form):
    username = forms.CharField(label='Username', required=False)
    displayname = forms.CharField(label='Name', required=False)
    host = forms.CharField(label='Host', required=False)
    url = forms.CharField(label='Host', required=False)
    github = forms.CharField(label='Github', required=False)
    id = forms.CharField(label='Id', required=False)


class UnFriendUserForm(forms.Form):
    username = forms.CharField(label='username', required=False)


class FriendRequestForm(forms.Form):
    def __init__(self, names, *args, **kwargs):
        super(FriendRequestForm, self).__init__(*args, **kwargs)
        CHOICES = (
            ('A', 'Accept'),
            ('R', 'Reject'),
        )
        for field_name in names:
            self.fields[field_name] = forms.CharField(max_length=32)
            self.fields[field_name] = forms.ChoiceField(
                label=field_name,
                choices=CHOICES,
                widget=forms.RadioSelect()
            )
