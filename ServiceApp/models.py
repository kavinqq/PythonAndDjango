from django.db import models
from django.contrib.auth.models import AbstractUser

# 用來記錄 客服員工資料
class Staff(AbstractUser):
    '''
    員工資料
    '''
    IdCard = models.CharField(max_length = 100, verbose_name = '身分證', help_text = '身分證')
    phone_number = models.CharField(max_length = 100, verbose_name = '手機號碼', help_text = '手機號碼')
    authority = models.IntegerField(default = 10, verbose_name = '權限', help_text = '數字越小 權限越大 superuser = -1')
    can_reset_password = models.BooleanField(default = False, verbose_name = '權限：重置密碼', help_text = '是否能 重置密碼')
    can_unlock = models.BooleanField(default = False, verbose_name = '權限：解鎖帳號', help_text = '是否能 解鎖帳號')
    can_search_username = models.BooleanField(default = False, verbose_name = '權限：查詢帳號', help_text = '是否能 查詢帳號')
    can_check_status = models.BooleanField(default = False, verbose_name = '權限：查看狀態', help_text = '是否能 查看會員狀態')
    can_new_employee = models.BooleanField(default = False, verbose_name = '權限：新增員工', help_text = '是否能 新增員工')
