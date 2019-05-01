from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from HappyShopping.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    VerifyCode：模型类code,mobile两个字段值都是必填
    发送验证码只传递了mobile字段值，所以不适合直接使用serializers.ModelSerializer
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证单个字段方法
        验证手机号码
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        # 验证手机号码合法性
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证码发送平率限制
        # # 获取1分钟前的时间点
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 验证码创建时间距离本次请求时间大于一分钟，抛出错误
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile):
            raise serializers.ValidationError('请勿频繁操作')

        # 将验证成功的手机返回，后面需要将其保存进数据库
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册
    """
    # write_only=True：序列化时将不会对该字段进行序列化返回
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码',
                                 error_messages={
                                     "blank": "验证码不能为空",  # 没有返回该字段时校验
                                     "required": "请输入验证码",  # 该字段值返回为空时校验
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, help_text='请输入验证码')
    # validators：自定义验证
    # UniqueValidator：唯一性验证
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="用户已经存在")])

    # 密码输入框加密
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, label='密码')

    # 此处也可以通过信号量来实现对密码加密
 #    def create(self, validated_data):
 #        """
 #        对用户输入密码进行加密
 #        如果没有重载该方法，用户注册的账户密码在数据库将会以明文保存
 #        """
 #        user = super(UserRegSerializer, self).create(validated_data=validated_data)
 #        user.set_password(validated_data['password'])
 #        user.save()
 #        return user

    def validate_code(self, code):
        # 用户前端传送过来的值都会被放在initial_data这个变量中
        # 用户多次发送只取最新的作为验证
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            # 验证码有效期5分钟
            """
            未过期：
            假设验证码创建时间(last_record.add_time)：10：05
            验证码验证时间：10：06
            验证时间前5分钟(five_mintes_ago)：10：01
            
            过期：
            假设验证码创建时间(last_record.add_time)：10：05
            验证码验证时间：10：12
            验证时间前5分钟(five_mintes_ago)：10：07
            """
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')

            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            # 该手机没有发送过验证码记录
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        """
        全局验证器
        :param attrs: 保存了前端传送过来的所有字段值
        :return:
        """
        # 由于前端仅传递过来了username和code字段值，而用户模型类中需要保存用户手机号，所以手动将username值传递给mobile
        attrs['mobile'] = attrs['username']
        # 由于用户模型类中不需要code字段，所以code字段仅作验证使用，使用完之后将其删除
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
