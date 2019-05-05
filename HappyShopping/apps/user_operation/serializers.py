from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator


class UserFavSerializer(serializers.ModelSerializer):
    """用户收藏序列化"""

    # 获取当前登录用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav

        # 可以作用在Meta外，对单个字段验证
        # 此处需要联合索引，需要至少两个字段，所以写在Meta内
        # 设置了联合索引后，当用户收藏同一件商品两次时就会抛出异常
        # 也可以在model模型类的Meta属性中添加：unique_together = ("user", "goods")
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user", "goods"),
                message="已收藏"
            )
        ]

        # 如果要有删除功能，则需要返回id字段
        fields = ("user", "goods", "id")
