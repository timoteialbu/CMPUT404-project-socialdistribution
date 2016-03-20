from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid


def create_uuid(sender, **kw):
        user = kw["instance"]
        if kw["created"]:
                userinfo = Author(user=user)
                userinfo.save()
post_save.connect(create_uuid, sender=User, dispatch_uid="users-uuidcreation-signal")


# TODO add UUID to User
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    displayName = models.CharField(max_length=30)
    url = models.URLField()
    github = models.URLField()
    def getUserName(self):
        u = User.objects.get(user)
        return u.username

class Post(models.Model):
    author = models.ForeignKey(
        Author, related_name='posts', on_delete=models.CASCADE)
    title = models.TextField(max_length=100, default="Untitled")
    source = models.URLField(max_length=200, blank=True)
    origin = models.URLField(max_length=200, blank=True)
    description = models.TextField(max_length=100, blank=True)
    content = models.TextField(max_length=4000)
    published = models.DateTimeField(auto_now_add=True)
    # TODO categories
    categories = ["web", "tutorial"]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        max_length=10, choices=PRIVACY_CHOICES, default='PRIVATE')

    # def save(self, *args, **kwargs):
    # mights be handy for setting publish and such
    def __unicode__(self):
        return self.content[:20] + "..."
    def getDisplayName(self):
        a = Author.objects.get(author)
        return a.getUserName

def image_file_name(instance, filename):
    return '/'.join(['images/uploads', str(uuid.uuid4()), filename])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField(max_length=400)
    published = models.DateTimeField('date published')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CONTENT_CHOICES = (
                      ('text/plain', 'Plain text'),
                      ('text/x-markdown', 'Markdown'),
    )
    contentType = models.CharField(
        max_length=16, choices=CONTENT_CHOICES, default='text/plain')

    def __unicode__(self):
        return self.comment[:20] + "..."


class Image(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateTimeField('date published')
    img = models.ImageField(upload_to=image_file_name)

    def __unicode__(self):
        return '%s' % (self.img)


class Node(models.Model):
    title = models.CharField(max_length=100)
    location = models.URLField(max_length=200)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    def __unicode__(self):
        return '%s' % (self.title)



