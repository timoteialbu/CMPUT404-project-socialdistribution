from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid


def create_uuid(sender, **kw):
        user = kw["instance"]
        if kw["created"]:
                userinfo = UserInfo(user=user)
                userinfo.save()
post_save.connect(create_uuid, sender=User, dispatch_uid="users-uuidcreation-signal")


# TODO add UUID to User
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Post(models.Model):
    author = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    source = models.URLField(max_length=200, blank=True)
    origin = models.URLField(max_length=200, blank=True)
    description = models.TextField(max_length=100, blank=True)
    content = models.TextField(max_length=4000)
    published = models.DateTimeField(auto_now_add=True)
    # TODO categories
    categories = ["web", "tutorial"]
    identity = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PRIVACY_CHOICES = (
                      ('PUBLIC', 'Public'),
                      ('FOAF', 'Friend of a Friend'),
                      ('FRIENDS', 'Private To My Friends'),
                      ('PRIVATE', 'Private To Me'),
                      ('SERVERONLY', 'Private To Friends On My Host'),
    )
    CONTENT_CHOICES = (
                      ('text/plain', 'Plain text'),
                      ('text/x-markdown', 'Markdown'),
    )
    contentType = models.CharField(
        max_length=16, choices=CONTENT_CHOICES, default='text/plain')
    visibility = models.CharField(
        max_length=10, choices=PRIVACY_CHOICES, default='ME')

    # def save(self, *args, **kwargs):
    # mights be handy for setting publish and such
    def __unicode__(self):
        return self.content[:20] + "..."


def image_file_name(instance, filename):
    return '/'.join(['images/uploads', str(uuid.uuid4()), filename])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=400)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.comment_text[:20] + "..."


class Image(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    img = models.ImageField(upload_to=image_file_name)

    def __unicode__(self):
        return '%s' % (self.img)
