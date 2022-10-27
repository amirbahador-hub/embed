from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from embed.common.services import model_update

from embed.users.models import BaseUser, Profile


def user_create(
    *,
    email: str,
    username: str,
    is_active: bool = True,
    is_admin: bool = False,
    password: Optional[str] = None,
) -> BaseUser:
    user = BaseUser.objects.create_user(
        email=email,
        username=username,
        is_active=is_active,
        is_admin=is_admin,
        password=password,
    )

    return user


def profile_create(
    *,
    bio: Optional[str] = None,
    user: BaseUser,
) -> QuerySet[Profile]:

    profile = Profile.objects.create(
        user=user,
        bio=bio,
    )

    return profile


@transaction.atomic
def register(
    *,
    username: str,
    email: str,
    password: str,
    bio: str,
) -> QuerySet[Profile]:

    user = user_create(
        username=username,
        email=email,
        is_active=True,
        is_admin=False,
        password=password,
    )
    profile = profile_create(user=user, bio=bio)

    return user


@transaction.atomic
def user_update(*, user: BaseUser, data) -> BaseUser:
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(
        instance=user, fields=non_side_effect_fields, data=data
    )

    return user
