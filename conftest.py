import pytest

from tests.factories import (
        BaseUserFactory,
        ProfileFactory,
        SubscriptionFactory,
        PostFactory,
        )

@pytest.fixture
def user1():
    return BaseUserFactory()

@pytest.fixture
def user2():
    return BaseUserFactory()

@pytest.fixture
def profile1(user1):
    return ProfileFactory(user=user1)


@pytest.fixture
def subsctiption1(user1, user2):
    return SubscriptionFactory(target=user1, subscription=user2)


@pytest.fixture
def post1(user1):
    return PostFactory(author=user1)
