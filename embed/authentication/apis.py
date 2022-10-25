from rest_framework.views import APIView
from rest_framework.response import Response

from embed.api.mixins import ApiAuthMixin

from embed.users.selectors import user_get_login_data


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        return Response(data)
