from django import forms
from django.contrib.auth.models import User
from .models import Post, Image

# i dont know what meta does ?
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text', 'privacy')


class UploadImgForm(forms.ModelForm):
    class Meta:
        model = Image
        # img = forms.ImageField(
        #    label = 'Select a Image',
        # )
        fields = ('title', 'img')

        
class UserChoiceForm(forms.Form):
    user_choice_field = forms.ModelChoiceField(queryset=User.objects.all())
    fields = ('username',)
