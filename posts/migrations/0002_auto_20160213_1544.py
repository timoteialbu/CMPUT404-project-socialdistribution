# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='privacy',
            field=models.CharField(default=b'ME', max_length=2, choices=[(b'ME', b'Private To Me'), (b'AU', b'Private To Another Author'), (b'FR', b'Private To My Friends'), (b'HO', b'Private To Friends On My Host'), (b'PU', b'Public')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
