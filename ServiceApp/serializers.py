from contextlib import nullcontext
from django.forms import PasswordInput
from rest_framework import serializers
from .models import Staff

# 客服員工登入用
class StaffLoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# 新增員工用
class AddStaffSerializers(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('username','password','staffId','IdCard','phoneNumber')


# 用戶輸入驗證資料用
class UserDataSerializers(serializers.Serializer):

    username = serializers.CharField(allow_blank = True)    
    id_card = serializers.CharField()    
    date_of_birth = serializers.CharField()
    mobile_number = serializers.CharField()

# 用戶輸入驗證資料用
class FrogetUserNameSerializers(serializers.Serializer):

    id_card = serializers.CharField()    
    date_of_birth = serializers.CharField()
    mobile_number = serializers.CharField()


# 回傳資料用
class RetrieveDataSerializers(serializers.Serializer):

    code = serializers.CharField(allow_blank = True,allow_null = True)
    message = serializers.CharField(allow_blank = True,allow_null = True)
    data = serializers.CharField(allow_blank = True,allow_null = True)


# CheckAccount回傳資料用
class RetrieveCheckAccountSerializers(serializers.Serializer):

    code = serializers.CharField(allow_blank = True,allow_null = True)
    message = serializers.CharField(allow_blank = True,allow_null = True)
    data = serializers.BooleanField(allow_null = True)
