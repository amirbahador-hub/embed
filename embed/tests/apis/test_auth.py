import pytest
from django.test import Client
from rest_framework.test import APIClient
from django.urls import reverse
from embed.users.models import BaseUser
import json


@pytest.mark.django_db
def test_unauth_post_api(user1, subscription1, profile1, post1):
    client = Client()
    url_ = reverse("api:blog:post")
            
    response = client.post(url_, content_type='application/json')

    assert response.status_code == 401


@pytest.mark.django_db
def test_login(user1, subscription1, profile1, post1):
    user = BaseUser.objects.create_user(username='john', email='js@js.com', password='js.sj')

    client = APIClient()
    url_ = reverse("api:authentication:jwt:login")
    body = {
            "username":user.username,
            "password":"js.sj"
            }
    response = client.post(url_, json.dumps(body), content_type='application/json')
    auth = json.loads(response.content)
    access = auth.get("access")
    refresh = auth.get("refresh")

    assert access != None
    assert type(access) == str
    
    assert refresh != None
    assert type(refresh) == str
 