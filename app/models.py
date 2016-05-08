from django.contrib.auth.models import User
from django.db import models

from .validators import is_zipfile


class Application(models.Model):
    author = models.ForeignKey(User)
    description = models.TextField()
    zip_file = models.FileField(upload_to="zip_files", validators=[is_zipfile])
    is_private = models.BooleanField(default=True)
