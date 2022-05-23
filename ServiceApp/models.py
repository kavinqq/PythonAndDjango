from django.db import models
from django.contrib.auth.models import AbstractUser

# 用來記錄 客服員工資料
class Staff(AbstractUser):
    staffId = models.CharField(max_length=100)
    IdCard = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
