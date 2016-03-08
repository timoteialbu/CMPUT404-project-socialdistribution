from django import forms
from django.contrib.auth.models import User
from friendship.models import Friend, Follow
from .models import Post, Image, Comment

# i dont know what meta does ?
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text', 'privacy')

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment_text',)


class UploadImgForm(forms.ModelForm):
    class Meta:
        model = Image
        # img = forms.ImageField(
        #    label = 'Select a Image',
        # )
        fields = ('title', 'img')

        
class AddFriendForm(forms.Form):
    user_choice_field = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
    )
    fields = ('username',)

# add checks if user exists
class UnFriendUserForm(forms.Form):
    username = forms.CharField(label='username', required=False)

