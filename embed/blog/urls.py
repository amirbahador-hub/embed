from django.urls import path
from .apis import PostApi

app_name = "blog"
urlpatterns = [
        path("post/", PostApi.as_view(), name="post")
        ]
