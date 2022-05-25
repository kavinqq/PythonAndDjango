from django.db import models
from django.contrib.auth.models import AbstractUser

# 用來記錄 客服員工資料
class Staff(AbstractUser):
    #身分證
    IdCard = models.CharField(max_length=100)
    #手機號碼
    phoneNumber = models.CharField(max_length=100)
    #權限 數字小  權限高
    authority = models.IntegerField(default=10)
    #是否能 重置密碼
    can_reset_password = models.BooleanField(default=False)
    #是否能 解鎖
    can_unlock = models.BooleanField(default=False)
    #是否能 找帳號
    can_search_username = models.BooleanField(default=False)
    #是否能 查看會員狀態
    can_check_status = models.BooleanField(default=False)
