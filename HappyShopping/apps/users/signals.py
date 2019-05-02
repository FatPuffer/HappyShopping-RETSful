from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# sender:接收哪个模型类的信号
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    """
    created:新建还是更新
    instance:我们传递过来的模型类
    """
    if created:
        # 新建
        password = instance.password
        instance.set_password(password)
        instance.save()

# 强调：一定不要忘记在所属应用apps.py文件中重载ready方法


