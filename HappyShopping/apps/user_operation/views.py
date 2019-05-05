from rest_framework import viewsets
from rest_framework import mixins

from .models import UserFav
from .serializers import UserFavSerializer


class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    用户收藏：发送post请求  http://127.0.0.1:8000/userfavs/1
    取消收藏：发送delete请求  http://127.0.0.1:8000/userfavs/1
    """
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

