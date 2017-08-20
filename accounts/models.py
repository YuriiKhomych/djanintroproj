from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from utils import get_file_path, validate_phone


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField('Email address', unique=True)
    phone = models.CharField(max_length=13, null=True, blank=True,
                             validators=[validate_phone])
    photo = models.FileField(upload_to=get_file_path)
    birthday = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
