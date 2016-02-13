from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post_text = models.CharField(max_length=400)
	pub_date = models.DateTimeField('date published')
	PRIVACY_CHOICES = (
		('ME', 'Private To Me'),
		('AU', 'Private To Another Author'),
		('FR', 'Private To My Friends'),
		('HO', 'Private To Friends On My Host'),
		('PU', 'Public'),
	)
        privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES, default='ME')
	def __unicode__(self):
		return self.post_text[:20] + "..."
	

