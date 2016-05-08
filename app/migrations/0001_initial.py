# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('description', models.TextField()),
                ('zip_file', models.FileField(validators=[app.validators.is_zipfile], upload_to='zip_files')),
                ('is_private', models.BooleanField(default=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
