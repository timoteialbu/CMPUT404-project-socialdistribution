from django.db.models.signals import  post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from api.models import Author
import os.path


@receiver(post_save, sender=User)
def create_uuid(sender, **kw):
	user = kw["instance"]
	if kw["created"]:
		userinfo = Author(user=user)
		userinfo.save()
post_save.connect(create_uuid, sender=User, dispatch_uid="users-uuidcreation-signal")

 
