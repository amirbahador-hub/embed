from embed.blog.models import Post, Subscription
from django.db.models import QuerySet
from embed.users.models import BaseUser
from django.utils.text import slugify


def subscribe(*, user:BaseUser, username:str) -> QuerySet[Subscription]:
    target = BaseUser.objects.get(username=username)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    return sub

def unsubscribe(*, user:BaseUser, username:str) -> dict:
    target = BaseUser.objects.get(username=username)
    return Subscription.objects.get(subscriber=user, target=target).delete()

def create_post(*, user: BaseUser, title: str, content: str) -> QuerySet[Post]:
    return Post.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )
