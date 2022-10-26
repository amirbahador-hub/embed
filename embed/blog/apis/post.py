from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema

from embed.api.pagination import get_paginated_response, LimitOffsetPagination

from embed.blog.models import Post 
from embed.blog.selectors.posts import post_list 
from embed.blog.services.post import create_post 
from embed.api.mixins import ApiAuthMixin


class PostApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSerializer(serializers.Serializer):
        content = serializers.CharField(max_length=1000)
        title = serializers.CharField(max_length=100)

    class OutPutSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")

        class Meta:
            model = Post
            fields = ("author", "title", "content", "created_at", "updated_at")

        def get_author(self, post):
            return post.author.username

    @extend_schema(
        responses=OutPutSerializer,
        request=InputSerializer,
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = create_post(
                user=request.user,
                content=serializer.validated_data.get("content"),
                title=serializer.validated_data.get("title"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutSerializer(query).data)

    @extend_schema(
        responses=OutPutSerializer,
    )
    def get(self, request):
        query = post_list(user=request.user)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )
