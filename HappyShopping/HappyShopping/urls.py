"""HappyShopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import xadmin
from django.conf import settings  # 媒体文件
from django.views.static import serve  # 媒体文件
from rest_framework.documentation import include_docs_urls  # 文档
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token 

# from goods.views_base import GoodsListView
# from goods.views import GoodsListView
from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet

router = DefaultRouter()

# 配置goods url
router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置category url
router.register(r'categorys', CategoryViewSet, base_name="categorys")

# 注册发送短信验证码
router.register(r'codes', SmsCodeViewSet, base_name="codes")

# 用户注册
router.register(r'users', UserViewSet, base_name="users")

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),  # 媒体文件
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # 登录

    # 路由注册
    url(r'^', include(router.urls)),

    # drf自带的生成Token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口:该路径需要和前端对接一致
    url(r'^login/', obtain_jwt_token),

    # 文档接口
    url(r'docs/', include_docs_urls(title='乐购平台')),
]
