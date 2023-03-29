from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


class UserManager(BaseUserManager):

    def create_user(self, username=None, password=None, **kwargs):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(username=username, **kwargs)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
            role='sadmin',
            is_active=True,
            is_superuser=True,
        )
        return user

ROLES = [
    ('sadmin', 'Super Admin')
    ('company', 'Company')
    ('staff', 'Staff')
]

class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to='user/profile', blank=True, null=True)
    fk_role = models.CharField(max_length=50, choices=ROLES)
    is_superuser = models.BooleanField(default=False, verbose_name='superuser status')
    is_active = models.BooleanField(default=True, verbose_name='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


# Create your models here.

