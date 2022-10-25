from django.urls import path, include

from .apis import (
    UserMeApi,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 

urlpatterns = [
    path(
        'jwt/',
        include(([
            path(
                "login/",
                TokenObtainPairView.as_view(),
                name="login"
            ),
            path(
                "refresh/",
                TokenRefreshView.as_view(),
                name="token_refresh"
            ),
            path(
                "verify/",
                TokenVerifyView.as_view(),
                name="token_verify"
            ),
        ], "jwt"))
    ),
    path(
        'me/',
        UserMeApi.as_view(),
        name='me'
    )
]

