from django import forms
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, FriendshipRequest
from api.models import Post, Image, Comment


# i dont know what meta does ?
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'visibility')

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment',)


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
                choices=CHOICES,
                widget=forms.RadioSelect()
            )
