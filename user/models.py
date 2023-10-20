from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """docstring for UserManager."""

    def create_employee(self, email, name, password=None):
        if not email:
            raise ValueError("User must have email addess")

        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        if not email:
            raise ValueError("Superuser must have email addess")

        user = self.model(email=self.normalize_email(email), name=name)
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class UserModel(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
