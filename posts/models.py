from django.db import models
from django.contrib.auth.models import User
import uuid


class Post(models.Model):
        author = models.ForeignKey(User, related_name='posts',
                                   on_delete=models.CASCADE)
        # TODO post_text as markdown (auto-detect)
        post_text = models.TextField(max_length=400)
        pub_date = models.DateTimeField('date published')
        PRIVACY_CHOICES = (
                ('ME', 'Private To Me'),
                ('AU', 'Private To Another Author'),
                ('FR', 'Private To My Friends'),
                ('HO', 'Private To Friends On My Host'),
                ('PU', 'Public'),
        )
        privacy = models.CharField(
                max_length=2, choices=PRIVACY_CHOICES, default='ME')

        def __unicode__(self):
                return self.post_text[:20] + "..."


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
        author = models.ForeignKey(User, related_name='images',
                                   on_delete=models.CASCADE)
        pub_date = models.DateTimeField('date published')
        img = models.ImageField(upload_to=image_file_name)

        def __unicode__(self):
                return '%s' % (self.img)
