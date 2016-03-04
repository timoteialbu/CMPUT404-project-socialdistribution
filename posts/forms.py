from django import forms
from django.contrib.auth.models import User
from friendship.models import Friend, Follow
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

        
class AddFriendForm(forms.Form):
    user_choice_field = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
    )
    fields = ('username',)

# add checks if user exists
class UnFriendUserForm(forms.Form):
    username = forms.CharField(label='username', required=False)


class FriendRequestForm(forms.Form):
    users = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label="Notify and subscribe users to this post:")



# class DivisionRemovalForm(forms.Form):
#     class MultipleDivisionField(forms.ModelMultipleChoiceField):
#         def label_from_instance(self, obj):
#             url = reverse('organizer_division_view', kwargs={'div_pk': obj.pk})
#             label = '<a href="%s">%s</a>' % (url, obj.__unicode__())
#             return mark_safe(label)

#     divisions = MultipleDivisionField(queryset=[],
#                 widget=forms.CheckboxSelectMultiple())

#     def __init__(self, competition, *args, **kwargs):
#         self.competition = competition
#         super(DivisionRemovalForm, self).__init__(*args, **kwargs)
#         self.fields['divisions'].queryset = self.competition.divisions.all()

#     def save(self):
#         for div in self.cleaned_data['divisions']:
#             units = div.units.all()
#             if units:
#                 for unit in units:
#                     unit.in_division = False
#                     unit.save()
#         divisions = self.cleaned_data['divisions']
#         divisions.delete()
