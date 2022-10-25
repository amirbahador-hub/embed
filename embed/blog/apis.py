from embed.blog.models import Post
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import serializers 
from embed.blog.selectors.posts import post_list
from embed.api.mixins import ApiAuthMixin


class PostApi(ApiAuthMixin, APIView):

    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ("content", "title")

    def get(self, request):
        query = post_list(user=request.user)
        serializer = self.OutPutSerializer(query, many=True)
        return Response(serializer.data)
