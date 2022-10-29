import factory

from tests.utils import faker
from embed.users.models import (
        BaseUser,
        Profile,
        )
from embed.blog.models import (
        Subscription,
        Post,
        )
from django.utils import timezone


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseUser

    username = factory.Iterator(["France", "Italy", "Spain"])
    email    = factory.Iterator(['fr@gmail.com', 'it@gmail.com', 'es@gmail.com'])
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    target        = factory.SubFactory(BaseUserFactory)
    subscriber    = factory.SubFactory(BaseUserFactory)

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post 

    title   = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    content = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    slug    = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    user    = factory.SubFactory(BaseUserFactory)

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user                 = factory.SubFactory(BaseUserFactory)
    created_at           = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    updated_at           = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    posts_count          = factory.LazyAttribute(lambda _: 0 )
    subscriptions_count  = factory.LazyAttribute(lambda _: 0 )
    subscribers_count    = factory.LazyAttribute(lambda _: 0 )
    bio                  = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
 
