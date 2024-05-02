from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from accounts.auth.helpers import valid_upto_date
from core.core.utils.tokens import generate_auth_token

# Create your models here.


class MyAccountManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email!")

        user = self.model(email=self.normalize_email(email),)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(primary_key=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perm(self, app_label):
        return self.is_superuser

    class Meta:
        db_table = 'accounts'


class TokenManager(models.Model):
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
    token = models.TextField(default=generate_auth_token, null=False, primary_key=True, db_index=True)
    valid_upto = models.DateTimeField(default=valid_upto_date, null=False)

    class Meta:
        db_table = 'access_tokens'
