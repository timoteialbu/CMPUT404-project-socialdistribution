from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from api.models import *
from rest_framework.authtoken.models import Token
import os.path


@receiver(post_save, sender=User)
def create_uuid(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        userinfo = Author(user=user)
        userinfo.save()


post_save.connect(create_uuid, sender=User, dispatch_uid="users-uuidcreation-signal")


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        print("Token Created")
        Token.objects.create(user=instance)


post_save.connect(create_auth_token, sender=User, dispatch_uid="user-auth")


@receiver(post_save, sender=Node)
def generate_token(sender, **kw):
    node = kw["instance"]
    if kw["created"]:
        print("token generated")
        user = node.user
        token = Token.objects.get(user=user)
        node.outgoing_token = token.key
        node.save()


post_save.connect(generate_token, sender=Node, dispatch_uid="gen_token_signal")
