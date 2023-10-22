import os
import jwt
import bcrypt
from django.db import models
from django.core.cache import cache
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
        user.role = 'admin'
        user.set_password(password)
        user.save(using=self._db)

        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=15, choices=[
                            ('admin', 'admin'), ('employee', 'employee')], default='employee')

    class Meta:
        db_table = 'user'

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed_password.decode("utf-8")

        return

    def check_password(self, password):
        check_correct = bcrypt.checkpw(password.encode(
            "utf-8"), self.password.encode("utf-8"))

        return check_correct

    def create_token(self):
        token = jwt.encode({"id": self.id, "email": self.email,
                           "name": self.name, "role": self.role}, os.environ.get('JWT_SECRET'), algorithm="HS256")

        cache.set(token, self.id, timeout=86400)

        return token

    def __str__(self):
        return self.email
