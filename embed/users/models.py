from django.db import models
from django.contrib.auth.models import (
    BaseUserManager as BUM,
    PermissionsMixin,
    AbstractBaseUser
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from embed.common.models import BaseModel
from django.utils.translation import gettext_lazy as _


class BaseUserManager(BUM):
    def create_user(self, username, email, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            username=username,
            is_admin=is_admin
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
            username=username,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user                = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    posts_count         = models.PositiveIntegerField(default=0)
    subscriptions_count = models.PositiveIntegerField(default=0)
    subscribers_count   = models.PositiveIntegerField(default=0)
    bio                 = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username} >>> {self.bio}"

