from embed.blog.models import Post, Subscription
from django.db.models import QuerySet
from embed.users.models import BaseUser, Profile
from django.utils.text import slugify
from django.db import transaction


def count_subs(*, user:BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()

def count_following(*, user:BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()

def count_posts(*, user:BaseUser) -> int:
    return Post.objects.filter(author=user).count()

def subscribe(*, user:BaseUser, username:str) -> QuerySet[Subscription]:
    target = BaseUser.objects.get(username=username)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    return sub

def unsubscribe(*, user:BaseUser, username:str) -> dict:
    target = BaseUser.objects.get(username=username)
    return Subscription.objects.get(subscriber=user, target=target).delete()

@transaction.atomic
def create_post(*, user: BaseUser, title: str, content: str) -> QuerySet[Post]:
    post = Post.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )
    profile = Profile.objects.get(user=user)
    profile.posts_count = count_posts(user=user)
    profile.save()

    return post
