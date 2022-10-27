from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from drf_spectacular.utils import extend_schema

from django.core.validators import MinLengthValidator 

from embed.api.pagination import get_paginated_response, LimitOffsetPagination

from embed.users.selectors import user_list
from embed.users.services import register
from embed.users.models import BaseUser
from embed.users.validators import integer_validator, alphabet_validator, special_characters_validator


class RegisterApi(APIView):

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("email", "username")

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


class UserListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        # Important: If we use BooleanField, it will default to False
        is_admin = serializers.NullBooleanField(required=False)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = (
                'id',
                'email',
                'is_admin'
            )

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self
        )
