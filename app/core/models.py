from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.EmailField(max_length=255)
    last_name = models.EmailField(max_length=255)
