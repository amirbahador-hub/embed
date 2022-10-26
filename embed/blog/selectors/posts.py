from django.db.models import QuerySet
from embed.blog.models import Post, Subscription
from embed.users.models import BaseUser


def get_subscribers(*, user:BaseUser) -> QuerySet[Subscription]:
    return Subscription.objects.filter(subscriber=user)


def post_list(*, user:BaseUser, self_include:bool = True) -> QuerySet[Post]:
    subscribtions = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscribtions.append(user.id)
    if subscribtions:
        return Post.objects.filter(author__in=subscribtions)
    return Post.objects.none()
