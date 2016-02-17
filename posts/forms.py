from django import forms

from .models import Post, Image


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
