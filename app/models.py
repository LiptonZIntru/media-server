from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        """
        Creates and saves a User with the given username, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Users must have an username')
        user = self.model(username=username, password=make_password(password))
        user.save()
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.model(username=username, password=make_password(password))
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()


class Film(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    duration = models.CharField(max_length=50)
    description = models.TextField(null=True)
    csfd_link = models.CharField(max_length=150, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    film_url = models.CharField(max_length=100, unique=True)


class FilmViewed(models.Model):
    id = models.IntegerField(primary_key=True)
    duration = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
