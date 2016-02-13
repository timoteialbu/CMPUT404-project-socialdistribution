from django.db import models

class Post(models.Model):
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	post_text = models.CharField(max_length=400)
	pub_date = models.DateTimeField('date published')
	PRIVACY = (
		('ME', 'Private To Me'),
		('AU', 'Private To Another Author'),
		('FR', 'Private To My Friends'),
		('HO', 'Private To Friends On My Host'),
		('PU', 'Public'),
	)
	def __unicode__(self):
		return self.post_text[:20] + "..."
	

