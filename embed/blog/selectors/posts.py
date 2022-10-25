from django.db.models import QuerySet
from embed.blog.models import Post, Subscription
from embed.users.models import BaseUser


def post_list(*, user:BaseUser) -> QuerySet[Post]:
    subscribtions = Subscription.objects.filter(subscriber=user).values_list("target", flat=True)
    if subscribtions:
        print(50*"-")
        print(subscribtions)
        return Post.objects.filter(author__in=subscribtions)
    return Post.objects.none()
