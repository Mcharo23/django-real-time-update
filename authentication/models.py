from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    username = None

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_authentication_user_set",
        related_query_name="custom_authentication_user",
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_authentication_user_set",
        related_query_name="custom_authentication_user",
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
