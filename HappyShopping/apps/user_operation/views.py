from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated  # 要求用户必须登录
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from utils.permissions import IsOwnerOrReadOnly  # 登录用户仅能操作自己的商品收藏
from .serializers import UserFavSerializer


class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    用户收藏：发送post请求  http://127.0.0.1:8000/userfavs/1
    取消收藏：发送delete请求  http://127.0.0.1:8000/userfavs/1
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 默认使用pk，查询的是get_queryset过滤后的内容，不用担心返回所有收藏该商品的用户对象
    lookup_field = "goods_id"  # 根据商品收藏商品id来查找

    # 返回当前登录用户的收藏
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

