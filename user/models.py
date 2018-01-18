from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=128,unique=True,null=False,blank=False)
    password = models.CharField(max_length=128,null=False,blank=False)
    head = models.ImageField()
    age = models.IntegerField()
    sex = models.IntegerField()

    # 密码不能明文输入
    def save(self):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save()
