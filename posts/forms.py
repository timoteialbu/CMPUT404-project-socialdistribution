from django import forms
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, FriendshipRequest
from .models import Post, Image

# i dont know what meta does ?
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text', 'privacy')


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

# add checks if user exists
class UnFriendUserForm(forms.Form):
    username = forms.CharField(label='username', required=False)


#class FriendRequestForm(forms.Form):
#    users = forms.MultipleChoiceField(
#        widget=forms.CheckboxSelectMultiple,
#        label="Notify and subscribe users to this post:")

    
class FriendRequestForm(forms.Form):    
    def __init__(self, dynamic_field_names, *args, **kwargs):
        super(FriendRequestForm, self).__init__(*args, **kwargs)
        CHOICES = (
            ('A', 'Accept'),
            ('R', 'Reject'),
        )
        for field_name in dynamic_field_names:
            self.fields[field_name] = forms.CharField(max_length=32) 
            self.fields[field_name] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())


class MyForm(forms.Form):
    static_field_a = forms.CharField(max_length=32)
    static_field_b = forms.CharField(max_length=32)
    static_field_c = forms.CharField(max_length=32)

    def __init__(self, dynamic_field_names, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)

        for field_name in dynamic_field_names:
            self.fields[field_name] = forms.CharField(max_legth=32) 
