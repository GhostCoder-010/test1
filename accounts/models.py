from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django_countries.fields import CountryField
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
    ('team_lead', 'Team Lead')
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


class CompanyProfile(models.Model):
    fkAdmin = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='company/logo/')
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=25, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    pincode = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# Create your models here.

