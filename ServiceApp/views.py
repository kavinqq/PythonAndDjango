from turtle import update
import requests
import json
import time
from django.conf import settings
#TODO
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
#TODO
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#TODO
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from utils.constant import RestPwdUrl,JsonHeaders,UnlockUrl,ForgetUserNameUrl,CheckAccountUrl,indexHtml
from datetime import datetime

from .models import Staff
from .serializers import *

# 新增員工
@method_decorator(login_required, name='post')
class NewStaffView(GenericAPIView):

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
            ddata= {'show':True,'is_error':False,'code': 707,'message': '新增成功','data':""}
            return render(request,indexHtml,{'data':ddata,'iusers':Staff.objects.all()})
        else :
            ddata= {'show':True,'is_error':False,'code': 807,'message': '新增失敗','data':""}
            return render(request,indexHtml,{'data':ddata,'iusers':Staff.objects.all()})


# 輸入登入資訊
def inputAccountInfo(request):
    return render(request, 'login.html')

# 登入
class LoginView(APIView):

    def post(self, request):
        print("start login post")

        data = request.data
        serializers = StaffLoginSerializers(data = data)

        if not serializers.is_valid():   
            print("登入資料格式錯誤")
            return HttpResponseRedirect('/serviceapp/input/')         
        #     try:
        #         # 撈出對應名稱的資料
        #         DbData = Staff.objects.get(username = data['username'])
        #     except Exception as e:
        #         print("無效的使用者名稱")
        #         return HttpResponseRedirect('/serviceapp/input/')
        # else :
        #     print("登入資料格式錯誤")
        #     return HttpResponseRedirect('/serviceapp/input/')

        data = serializers.validated_data
        print("驗證帳密")
        user = authenticate(request, username = data['username'], password = data['password'])        
        dbuser = Staff.objects.get(username = data['username'])
        print(f" check pwd = {dbuser.check_password(data['password'])}")
        
        if user:
            print("成功")
            login(request, user)
            return HttpResponseRedirect('/serviceapp/index/')
        else :
            print("失敗")
            return HttpResponseRedirect('/serviceapp/input/')


#登出
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/serviceapp/input/')
    
    
#登入後跳轉
def TestAuth(request):
    try:
        user = Staff.objects.get(username = request.user.username)    
        return render(request,indexHtml,{"user":user,'iusers':Staff.objects.all()})
    except:        
        return render(request,indexHtml,{"user":"nononon",})

#主管修改下屬權限
class ChangePermissionView(GenericAPIView):
    serializer_class=PermissionSerializers
    def post(self,request):
        data=request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return render(request,indexHtml,{
                'data':{'show':True,'is_error':True,'code': 801,'message': '資料格式(待傳輸)驗證錯誤','data':serializer.error_messages},
            'iusers':Staff.objects.all()
            })

        data = serializer.validated_data
        user = Staff.objects.get(username=data['username'])
        user.authority=data['authority']
        user.can_reset_password=data['can_reset_password']
        user.can_unlock=data['can_unlock']
        user.can_search_username=data['can_search_username']
        user.can_check_status=data['can_check_status']
        user.save()
        return render(request,indexHtml,{
            'data':{'show':False,'is_error':False,'code': 705,
            'message': '修改成功','data':f"已修改使用者:{user.username}"},
        'iusers':Staff.objects.all()
        })

"""
APIView 父類別 start
"""
class ControlPostView(APIView):
    #rdata 接收 request
    def serializer_before_sent(self,rdata):
        print("start SBS")
        data = rdata.data
        serializer = UserDataSerializers(data , data)
        if not serializer.is_valid():
            return {'show':True,'is_error':True,'code': 801,'message': '資料格式(待傳輸)驗證錯誤','data':serializer.error_messages}
        data = serializer.validated_data
        return {'show':False,'is_error':False,'code': 701,'message': '資料格式(待傳輸)驗證通過','data':data}

    #radata 接收 dict
    def sent_receive_serializer(self,rdata,url_to_sent):
        print("start CRS")
        #建立要傳送的資料
        payload = json.dumps({
            "username": rdata['username'],
            "id_card": rdata['id_card'],
            "date_of_birth": rdata['date_of_birth'],
            "mobile_number": rdata['mobile_number'],            
        })
        #傳送並接收
        response = requests.request("POST", url_to_sent, headers = JsonHeaders, data = payload)
        #解析資料
        if response.status_code != 200:
            return {'show':True,'is_error':True,'code': 802,'message': '連線SSO出問題','data':response.text}
        response = json.loads(response.text)
        result = RetrieveDataSerializers(data=response)
        
        if not result.is_valid() :
            print("回傳資料驗證沒過")
            return {'show':True,'is_error':True,'code': 803,'message': '資料格式(接收)驗證錯誤','data':result.error_messages}
        
        valid_result = result.validated_data
        return {'show':True,'is_error':False,'code': valid_result['code'],'message': valid_result['message'],'data':valid_result['data']}
    
    def short_do(self, rr,url):
        data0=self.serializer_before_sent(rr)
        print(data0)
        if data0['is_error']:   
            print("待傳資料 驗證錯誤") 
            return data0
        else:
            data = self.sent_receive_serializer(data0['data'],url)
            return data

"""
APIView 父類別 end
"""
#重構start

#重置密碼
class RestPasswordView(ControlPostView): 
    def post(self, request):
        return render(request,indexHtml,{'data':self.short_do(request,RestPwdUrl),'iusers':Staff.objects.all()})

#解鎖
class UnlockView(ControlPostView):  
    def post(self, request):        
        return render(request,indexHtml,{'data':self.short_do(request,UnlockUrl),'iusers':Staff.objects.all()}) 

#查帳號
class ForgetUsernameView(ControlPostView): 
    def post(self, request):        
        return render(request,indexHtml,{'data':self.short_do(request,ForgetUserNameUrl),'iusers':Staff.objects.all()}) 

#查開戶
class CheckAccountView(ControlPostView): 
    def post(self, request):        
        return render(request,indexHtml,{'data':self.short_do(request,CheckAccountUrl),'iusers':Staff.objects.all()})

#重構end


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

#測試網頁
def Test3(request):    
    return render(request,indexHtml,{})

class IGCView(GenericAPIView):
    serializer_class= IGCSerializers
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response("資料錯誤",status=status.HTTP_200_OK)
        
        data=serializer.validated_data
        #這次操作來更改密碼
        print(f"username = {data['username']}")
        print(f"pwd = {data['password']}")
        user = Staff.objects.get(username=data['username'])
        user.set_password(data['password'])
        user.save()
        return Response("修改完成",status=status.HTTP_200_OK)

class TestTimes():
    test_times=0
    def add():
        TestTimes.test_times = TestTimes.test_times + 1

class TestTimes2():
    test_times=0
    def add():
        TestTimes2.test_times = TestTimes2.test_times + 1


#測試用 小def
def igc1(request):
    start = time.time()
    TestTimes.add()
    payload = json.dumps({
        "username": '',
        "id_card": 'A123456789',
        "date_of_birth": '2022-05-23',
        "mobile_number": '0987654321',            
    })
    times=10
    for i in range(times):
        r = requests.request("POST", RestPwdUrl, headers = JsonHeaders, data = payload)
        TestTimes2.add()
        time.sleep(100/1000)
    return HttpResponse(f'第{TestTimes.test_times}次惡作劇<br>\
                        傳送了{TestTimes2.test_times}次<br>\
                        耗時:{format(time.time()-start)}<br>\
                        最終內容:{r.text}')


#測試用小class
class IGC0View(APIView):
    def get(self,request):
        data0 = { #request的headers
            # 'keys':request.headers.keys(),
            'Content-Length':request.headers['Content-Length'],
            'Content-Type':request.headers['Content-Type'],
            'Host':request.headers['Host'],
            'Connection':request.headers['Connection'],
            #下面這個是啥?
            # 'Cache-Control':request.headers['Cache-Control'],
            'Upgrade-Insecure-Requests':request.headers['Upgrade-Insecure-Requests'],
            'User-Agent':request.headers['User-Agent'],
            'Accept':request.headers['Accept'],
            'Accept-Encoding':request.headers['Accept-Encoding'],
            'Accept-Language':request.headers['Accept-Language'],
            'Cookie':request.headers['Cookie'],
        }
        data1 = { #request other
            'session':request.session,
            'body':request.body, 
            'get_host':request.get_host(),
            'get_port':request.get_port(),
            'get_full_path':request.get_full_path(),
            'get_full_path_info':request.get_full_path_info(),
            'build_absolute_uri':request.build_absolute_uri(location=None),
            # 'site':request.site,
        }
        data2 = { #request user    
            'user':str(request.user),
        }
        strr = request.headers.get('Cookie')
        start=strr.find('csrftoken')+10
        end = strr
        data3 = { #csrf
            'csrf':strr[start:start+64]
        }
        data4 = { #try accept
            "request.accepts('text/html')":request.accepts('text/html')
        }
        data5 = {
            'readlines':request.readlines(),
            '__iter__':request.__iter__(),
        }
        data0.update(data1)
        data0.update(data3)
        data0.update(data4)
        time0 = datetime.strptime("2020-02-20","%Y-%m-%d")
        response0 = HttpResponse()
        response = HttpResponse(content=b'', content_type=None, status=200, reason=None, charset=None, headers=None)
        response['food']='apple'
        response.set_cookie(key='key0',value='value0',max_age=300,expires=time0,path='/',domain='www.googl.com',secure=False,httponly=False,samesite=None)
        data6 = {
            'response0.__dict__':response0.__dict__,
            'response.__dict__':response.__dict__,
            # 'items()':response.items(),
        }
        # return response
        return Response(data0)

