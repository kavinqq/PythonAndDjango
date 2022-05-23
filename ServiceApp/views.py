import re
import requests
import json

from logging import exception, raiseExceptions
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from .models import Staff
from .serializers import AddStaffSerializers, FrogetUserNameSerializers, RetrieveCheckAccountSerializers, RetrieveDataSerializers, StaffLoginSerializers,UserDataSerializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from .utils.constant import ServiceResponse,RestPwdUrl,JsonHeaders,UnlockUrl,ForgetUserNameUrl,CheckAccountUrl
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.shortcuts import render
from ServiceApp import serializers

# 新增員工
@method_decorator(login_required, name='post')
class NewStaff(GenericAPIView):

    queryset = Staff.objects.all()
    serializer_class = AddStaffSerializers        
    
    def post(self, request):

        data = request.data
        
        serializers = AddStaffSerializers(data=data)                

        # 驗證資料
        if serializers.is_valid(raise_exception=True):
            
            serializers.save()            

            #把存進去的密碼 改成 加密
            user = Staff.objects.get(username = data["username"])
            user.set_password(data['password'])
            user.save()

            return Response("新增員工成功", status=status.HTTP_200_OK)
        else :

            return Response("新增員工失敗", status=status.HTTP_200_OK)


# 輸入登入資訊
class inputAccountInfo(APIView):

    def get(self, request):
        return render(request, 'login.html')

# 登入
class Login(APIView):

    def post(self, request):
        print("start login post")

        data = request.data

        serializers = StaffLoginSerializers(data = data)

        if serializers.is_valid(raise_exception=True):            
            try:
                # 撈出對應名稱的資料
                DbData = Staff.objects.get(username = data['username'])

            except Exception as e:

                return Response("無效的使用者名稱!", status=status.HTTP_200_OK)

        else :

            return Response("登入資料格式錯誤!", status=status.HTTP_200_OK)

        data = serializers.validated_data
        print("驗證帳密")
        user = authenticate(request, username = data['username'], password = data['password'])        

        if user :
            print("成功")
            login(request, user)
            return HttpResponseRedirect('/ServiceApp/TestAuth/')
        else :
            print("失敗")
            return HttpResponseRedirect("/ServiceApp/TestAuth/")            


def TestAuth(request):
    try:
        user = Staff.objects.get(username = request.user.username)
    
        return render(request,'test2.html',{"user":user,})
    except:
        
        return render(request,'test2.html',{"user":"nononon",})
    #return HttpResponse(f"跳轉成功 {request.user.username}", status=status.HTTP_200_OK)
    

    



# 重置密碼
class RestPasswordView(APIView):

    #測試用post
    def post(self, request):

        # 接收需求夾帶的資料
        data = request.data        

        # 驗證資訊的序列化
        serializers = UserDataSerializers(data, data)        

        # 如果request夾帶的資料 不符合驗證 => 直接回傳
        if not serializers.is_valid():
            
            data = {'code': 999,'message': "沒有提供該服務 或 格式錯誤"}

            return Response(data, status=status.HTTP_200_OK)        

        # 拿到序列化驗證過後的資料
        data = serializers.validated_data        
        
        # 轉成json
        payload = json.dumps({
            "username": data['username'],
            "id_card": data['id_card'],
            "date_of_birth": data['date_of_birth'],
            "mobile_number": data['mobile_number'],            
        })
        
        # 發一個request      
        response = requests.request("POST", RestPwdUrl, headers = JsonHeaders, data = payload)
        
        # 如果是連線問題 
        if response.status_code != 200:
            return Response(f"連線問題 代碼:{response.status_code}",status=status.HTTP_200_OK)

        # 為什麼不能直接用 Serializers轉 要先轉成 json??
        response = json.loads(response.text)        

        result = RetrieveDataSerializers(data=response)


        if result.is_valid() :
            valid_result = result.validated_data
        else :
            return Response("回傳資料格式錯誤!")
        

        return Response(f"{valid_result.get('code')}  {valid_result.get('message')}  {valid_result.get('data')}", status=status.HTTP_200_OK)   
   

# 解鎖
class UnlockView(APIView):
        
    #測試用post
    def post(self, request):

        # 接收需求夾帶的資料
        data = request.data        

        # 驗證資訊的序列化
        serializers = UserDataSerializers(data = data)        

        # 如果request夾帶的資料 不符合驗證 => 直接回傳
        if not serializers.is_valid():
            
            data = {'code': 999,'message': "沒有提供該服務 或 格式錯誤", 'data': 'No data'}  

            return render(request, 'test.html', {"result" : data})

        # 拿到序列化驗證過後的資料
        data = serializers.validated_data        
        
        # 轉成json
        payload = json.dumps({
            "username": data['username'],
            "id_card": data['id_card'],
            "date_of_birth": data['date_of_birth'],
            "mobile_number": data['mobile_number'],            
        })
        
        # 發一個request      
        response = requests.request("POST", UnlockUrl, headers = JsonHeaders, data = payload)

        print(response.text)
        
        # 如果是連線問題 
        if response.status_code != 200:

            data = {'code': 999,'message': "發生連線錯誤", 'data': 'No data'}  

            return render(request, 'test.html', {"result" : data})
    
        response = json.loads(response.text)        

        result = RetrieveDataSerializers(data=response)


        if result.is_valid(raise_exception=True) :
            valid_result = result.validated_data
        else :            

            return render(request, 'test.html', {"result": {'code': 999,'message': "發生連線錯誤", 'data': 'No data'}})
        
        return render(request, "test.html", {"result" : valid_result})
        

# 忘記密碼
class ForgetUsernameView(APIView):
        
    #測試用post
    def post(self, request):

        # 接收需求夾帶的資料
        data = request.data        

        # 驗證資訊的序列化
        serializers = FrogetUserNameSerializers(data, data)        

        # 如果request夾帶的資料 不符合驗證 => 直接回傳
        if not serializers.is_valid():
            
            data = {'code': 999,'message': "沒有提供該服務 或 格式錯誤"}

            return Response(data, status=status.HTTP_200_OK)        

        # 拿到序列化驗證過後的資料
        data = serializers.validated_data     
        
        # 轉成json
        payload = json.dumps({            
            "id_card": data['id_card'],
            "date_of_birth": data['date_of_birth'],
            "mobile_number": data['mobile_number'],            
        })
        
        # 發一個request      
        response = requests.request("POST", ForgetUserNameUrl, headers = JsonHeaders, data = payload)
        
        # 如果是連線問題 
        if response.status_code != 200:
            return Response(f"連線問題 代碼:{response.status_code}",status=status.HTTP_200_OK)

        # 為什麼不能直接用 Serializers轉 要先轉成 json??
        response = json.loads(response.text)        

        result = RetrieveDataSerializers(data=response)

        if result.is_valid() :
            valid_result = result.validated_data
        else :
            return Response("回傳資料格式錯誤!")
        

        return Response(f"{valid_result.get('code')}  {valid_result.get('message')}  {valid_result.get('data')}", status=status.HTTP_200_OK) 


# 重置密碼
class CheckAccountView(APIView):
        
    #測試用post
    def post(self, request):

        # 接收需求夾帶的資料
        data = request.data        

        # 驗證資訊的序列化
        serializers = UserDataSerializers(data, data)        

        # 如果request夾帶的資料 不符合驗證 => 直接回傳
        if not serializers.is_valid():
            
            data = {'code': 999,'message': "沒有提供該服務 或 格式錯誤"}

            return Response(data, status=status.HTTP_200_OK)        

        # 拿到序列化驗證過後的資料
        data = serializers.validated_data        
        
        # 轉成json
        payload = json.dumps({
            "username": data['username'],
            "id_card": data['id_card'],
            "date_of_birth": data['date_of_birth'],
            "mobile_number": data['mobile_number'],            
        })
        
        # 發一個request      
        response = requests.request("POST", CheckAccountUrl, headers = JsonHeaders, data = payload)

        print(response.text)
        
        # 如果是連線問題 
        if response.status_code != 200:
            return Response(f"連線問題 代碼:{response.status_code}",status=status.HTTP_200_OK)

        # 為什麼不能直接用 Serializers轉 要先轉成 json??
        response = json.loads(response.text)        

        result = RetrieveCheckAccountSerializers(data=response)


        if result.is_valid() :
            valid_result = result.validated_data
        else :
            return Response("回傳資料格式錯誤!")
        

        return Response(f"{valid_result.get('code')}  {valid_result.get('message')}  {valid_result.get('data')}", status=status.HTTP_200_OK) 

    



#Member model get 測試
@login_required()
def Test(request): 

    # 測試用連結 (連結上面的GenericsAPIViw get() )
    url = "http://127.0.0.1:8000/Staff/?username=AAA&manageId=1"    

    # 接回傳
    response = requests.get(url)

    print(f'whats this? {response.status_code}')
    
    # 根據傳回來的驗證結果 給予對應提示
    if response.status_code == status.HTTP_200_OK:
        return HttpResponse("正確")
    else:
        return HttpResponse("錯誤")