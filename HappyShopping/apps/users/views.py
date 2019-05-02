from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from HappyShopping.settings import APIKEY
from random import choice
from django.contrib.auth import get_user_model

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler  # jwt生成Token模块

from .serializers import SmsSerializer, UserRegSerializer
from utils import yunpian
from .models import VerifyCode

User = get_user_model()


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    ViewSetMixin 内部实现了as_view()方法，让我们可以通过Router实现路由分发
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数的随机验证码
        """
        sends = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(sends))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # 如果获取参数为空，则抛出异常，错误状态吗400
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']

        # 短信发送验证码
        yun_pian = yunpian.YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        
        # 根据返回值判断短信发送是否成功，返回相应信息
        if sms_status.get('code') != 0:
            return Response({
                "mobile": sms_status.get("msg")   
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile    
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    注册成功跳转至登录页面：需要重载CreateModelMixin中的create方法，将Token一起返回前端
    """
    serializer_class = UserRegSerializer
    # 返回信息
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 获取用户对象
        user = self.perform_create(serializer)

        # 获取要返回数据
        re_dict = serializer.data

        # 生成payload载体
        payload = jwt_payload_handler(user)

        # 利用载体生成Token并协同数据一起返回
        re_dict['token'] = jwt_encode_handler(payload)

        # 将用户名一起返回
        re_dict['username'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 返回保存后的用户对象
        return serializer.save()
