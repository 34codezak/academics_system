from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Create your models here.
class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class UserManager(BaseUserManager):
    def get_object_by_name(self, name):
        try:
            instance = self.get(name=name)
            return instance

        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self, username, email, password=None, **kwargs):
        """
        Create and return a `User` with an email, phone number, and password.
        """

        if username is None:
            raise TypeError('User must have a username.')
        if email is None:
            raise TypeError('User must have an email.')
        if password is None:
            raise TypeError('User must have password.')


        user = self.model(username=username,
        email = self.normalize_email(email), *kwargs)
        user.set_password(password)
        user.save(using=self._db)
         
    def create_superuser(self, username, email, password, **kwargs):
        """ Create and return a `User` with superuser (admin) permissions. """
        if password is None:
            raise TypeError('Superuser must have a password.')
        if email is None:
            raise TypeError('Superuser must have and email.')
        if username is None:
            raise TypeError('Superuser must have a username.')

        

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user