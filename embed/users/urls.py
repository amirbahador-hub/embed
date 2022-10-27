from django.urls import path

from .apis import UserListApi, RegisterApi


urlpatterns = [
    path('', UserListApi.as_view(), name='list'),
    path('register/', RegisterApi.as_view(), name='register'),
]
