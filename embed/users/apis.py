from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from drf_spectacular.utils import extend_schema

from django.core.validators import MinLengthValidator 
from django.conf import settings
import jwt

from embed.api.pagination import get_paginated_response, LimitOffsetPagination

from embed.users.selectors import user_list, get_profile
from embed.users.services import register
from embed.users.models import BaseUser, Profile
from embed.users.validators import integer_validator, alphabet_validator, special_characters_validator


class ProfileApi(APIView):

    class OutPutProfileSerializer(serializers.ModelSerializer):

        user = serializers.SerializerMethodField("get_user")

        class Meta:
            model = Profile 
            fields = ("bio", "posts_count", "subscriptions_count", "subscribers_count", "user")

        def get_user(self, profile):
            return profile.user.username

    def get(self, request):
        query = get_profile(user=request.user)
        serializer = self.OutPutProfileSerializer(query)
        return Response(serializer.data)
 
class RegisterApi(APIView):

    class OutPutRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")
        class Meta:
            model = BaseUser
            fields = ("email", "username", "token")

        def get_token(self, user):
            decode = AccessToken.for_user(user)
            decode_dict = {"iat":decode["iat"], "jti":decode["jti"], "user_id":decode["user_id"],
                    "exp":decode["exp"], "token_type":decode["token_type"]}
            encoded = jwt.encode(decode_dict, settings.SECRET_KEY, algorithm="HS256")
            return encoded


    class InputRegisterSerializer(serializers.Serializer):

        username = serializers.CharField(max_length=100)
        email = serializers.EmailField()
        bio = serializers.CharField(max_length=200, required=False)
        password = serializers.CharField(validators=[integer_validator, alphabet_validator, special_characters_validator, MinLengthValidator(limit_value=10)])
        confirm_password = serializers.CharField()

         
        def validate_email(self, email):
            existing = BaseUser.objects.filter(email=email).first()
            if existing:
                raise serializers.ValidationError("Someone with that email "
                "address has already registered. Was it you?")
            return email

        def validate(self, data):
            if not data.get('password') or not data.get('confirm_password'):
                raise serializers.ValidationError("Please enter a password and "
                    "confirm it.")
            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError("Those passwords don't match.")
            return data


    @extend_schema(
            request=InputRegisterSerializer,
            responses=OutPutRegisterSerializer,
            )
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = register(
                username = serializer.validated_data.get("username"),
                password = serializer.validated_data.get("password"),
                email = serializer.validated_data.get("email"),
                bio = serializer.validated_data.get("bio"),
                )

        serializer_output = self.OutPutRegisterSerializer(user)
        return Response(serializer_output.data)

