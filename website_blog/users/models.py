from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from PIL import Image


class UserManager(BaseUserManager):

  def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
    if not username:
        raise ValueError('Users must have an username')
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        username=username,
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, email, password, **extra_fields):
    return self._create_user(username, email, password, False, False, **extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    user=self._create_user(username, email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=254, unique=True, null=False)
    image = models.ImageField(upload_to='profile_picture/', default='default.jpg', blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def save(self,*args,**kwargs):
      super().save(*args,**kwargs)

      img = Image.open(self.image.path)

      if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)