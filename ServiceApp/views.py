import requests
import json
import time

from django.conf import settings
#TODO
from django.http import HttpResponse, HttpResponseRedirect
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

from datetime import datetime

from .models import Staff
from .serializers import *
from global_settings.enums import *
from utils.constant import *

# 新增員工
@method_decorator(login_required, name = 'post')
class NewStaffView(GenericAPIView):

    serializer_class = AddStaffSerializers

    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data = data)

        # 驗證資料
        if not serializer.is_valid():
            parameter = {
                'data': CodeMessageEnum.ADD_NEW_EMPLOYEE_FAILED.to_dict(),
                'iusers': Staff.objects.all()
            }
            return render(request, indexHtml, parameter)    #驗證傳入的資料失敗 return

        data = serializer.validated_data
        #在model創建rowdata的好方法
        Staff.objects.create(**data)
        parameter = {
            'data': CodeMessageEnum.ADD_NEW_EMPLOYEE_SUCCESS.to_dict(),
            'iusers': Staff.objects.filter(authority__gt = request.user.authority),
        }
        return render(request, indexHtml, parameter)    #驗證傳入的資料成功 return


"""
APIView 父類別 start--------------------------
"""
class ControlPostView(APIView):
    #rdata 接收 request
    def serializer_before_sent(self,rdata):
        print('start SBS')
        data = rdata.data
        serializer = UserDataSerializers(data, data)
        if not serializer.is_valid():
            return CodeMessageEnum.VALIDATION_FAILED.to_dict(serializer.error_messages) #傳入的資料格式驗證錯誤 return

        data = serializer.validated_data
        return CodeMessageEnum.VALIDATION_SUCCESS.to_dict(data) #傳入資料驗證正確 return

    #radata 接收 dict
    def sent_receive_serializer(self, rdata, url_to_sent):
        print('start CRS')
        #建立要傳送的資料
        payload = json.dumps({
            'username': rdata.get('username'),
            'id_card': rdata.get('id_card'),
            'date_of_birth': rdata.get('date_of_birth'),
            'mobile_number': rdata.get('mobile_number'),
        })

        #傳送並接收
        response = requests.request('POST', url_to_sent, headers = JsonHeaders, data = payload)

        #解析資料
        if response.status_code != 200:
            print(CodeMessageEnum.CONNECT_TO_SSO_FAILED.message)
            return CodeMessageEnum.CONNECT_TO_SSO_FAILED.to_dict(response.text) #連線到SSO失敗 return

        response = json.loads(response.text)
        result = RetrieveDataSerializers(data = response)

        if not result.is_valid():
            print(CodeMessageEnum.RECEIVE_DATA_VALID_FAILED.message)
            return CodeMessageEnum.RECEIVE_DATA_VALID_FAILED.to_dict(result.error_messages) #從SSO回傳的資料格式驗證錯誤 return

        valid_result = result.validated_data
        return {**valid_result, 'is_error': False}  #回傳資料驗證成功 return

    def short_do(self, request, url_to_exe):
        data0 = self.serializer_before_sent(request)
        print(data0)
        if data0.get('is_error'):
            print('待傳資料 驗證錯誤')
            return data0    #傳出前階段發生錯誤 return
        else:
            data = self.sent_receive_serializer(data0.get('data'), url_to_exe)
            return data     #把接收資料後的結果回傳 return

"""
APIView 父類別 end--------------------------
"""
#重構start-----------------------
#重置密碼
class RestPasswordView(ControlPostView):
    def post(self, request):
        # TODO 做成完成作業後跳轉回 index/
        # request
        # data0=self.short_do(request,RestPwdUrl)
        # print(f"data0={data0}")
        # return redirect('/serviceapp/index/',kwargs={'data':data0})
        # return redirect('/serviceapp/index/',permanent=True, data=data0,iusers=Staff.objects.all())
        return render(request, indexHtml, {
            'data': self.short_do(request, RestPwdUrl),
            'iusers': Staff.objects.filter(authority__gt = request.user.authority),
        })


#解鎖
class UnlockView(ControlPostView):
    def post(self, request):
        return render(request, indexHtml, {
            'data': self.short_do(request, UnlockUrl),
            'iusers': Staff.objects.filter(authority__gt = request.user.authority),
        }) 


#查帳號
class ForgetUsernameView(ControlPostView):
    def post(self, request):
        return render(request, indexHtml, {
            'data': self.short_do(request, ForgetUserNameUrl),
            'iusers': Staff.objects.filter(authority__gt = request.user.authority),
        })


#查開戶
class CheckAccountView(ControlPostView):
    def post(self, request):
        return render(request, indexHtml, {
            'data': self.short_do(request, CheckAccountUrl),
            'iusers': Staff.objects.filter(authority__gt = request.user.authority),
        })
#重構end-----------------------


# 輸入登入資訊
def page_to_login(request):
    return render(request, 'login.html')


# 登入
class LoginView(APIView):

    def post(self, request):
        print('start login')

        data = request.data
        serializers = StaffLoginSerializers(data = data)

        if not serializers.is_valid():
            print('登入資料格式錯誤')
            return HttpResponseRedirect('/serviceapp/input/')   #輸入的格式錯誤 return

        data = serializers.validated_data
        user = authenticate(request, username = data.get('username'), password = data.get('password'))
        dbuser = Staff.objects.get(username = data.get('username'))
        
        if not user:
            print('失敗')
            return HttpResponseRedirect('/serviceapp/input/')   #帳密錯誤 return

        print('成功')
        login(request, user)
        return redirect('/serviceapp/index/')   #成功登入 return


#登出
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/serviceapp/input/')
    
    
#登入後跳轉
def open_index_page(request):
    user = Staff.objects.get(username = request.user.username)
    if user:
        return render(request, indexHtml, {
                    'user': user,
                    'iusers': Staff.objects.all()
        })
    return render(request, indexHtml, {
                'user':'nononon',
    })


#主管修改下屬權限
class ChangePermissionView(GenericAPIView):
    serializer_class = PermissionSerializers
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        if not serializer.is_valid():
            return render(request, indexHtml, {
                        'data': {
                            'show': True,
                            'is_error': True,
                            'code': 801,
                            'message': '資料格式(待傳輸)驗證錯誤',
                            'data': serializer.error_messages
                        },
                        'iusers': Staff.objects.all()
            })

        data = serializer.validated_data
        user = Staff.objects.get(username = data.get('username'))
        user.authority = data.get('authority')
        user.can_reset_password = data.get('can_reset_password')
        user.can_unlock = data.get('can_unlock')
        user.can_search_username = data.get('can_search_username')
        user.can_check_status = data.get('can_check_status')
        user.save()
        return render(request, indexHtml, {
                    'data': {
                        'show': False,
                        'is_error': False,
                        'code': 705,
                        'message': '修改成功',
                        'data': f'已修改使用者:{user.username}'
                    },
                    'iusers': Staff.objects.all()
        })


#test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----
#test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----test-----
#Member model get 測試
@login_required()
def Test(request):

    # 測試用連結 (連結上面的GenericsAPIViw get() )
    url = 'http://127.0.0.1:8000/Staff/?username=AAA&manageId=1'

    # 接回傳
    response = requests.get(url)

    print(f'whats this? {response.status_code}')
    
    # 根據傳回來的驗證結果 給予對應提示
    if response.status_code == status.HTTP_200_OK:
        return HttpResponse('正確')
    else:
        return HttpResponse('錯誤')


#igc
class IGCView(GenericAPIView):
    serializer_class = IGCSerializers
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        if not serializer.is_valid():
            return Response('資料錯誤', status = status.HTTP_200_OK)
        
        data=serializer.validated_data
        #這次操作來更改密碼
        print(f'username = {data.get("username")}')
        print(f'pwd = {data.get("password")}')
        user = Staff.objects.get(username = data.get('username'))
        user.set_password(data.get('password'))
        user.save()
        return Response('修改完成', status = status.HTTP_200_OK)


class TestTimes():
    test_times = 0
    def add():
        TestTimes.test_times = TestTimes.test_times+1


class TestTimes2():
    test_times = 0
    def add():
        TestTimes2.test_times = TestTimes2.test_times+1


#igc1
def igc1(request):
    start = time.time()
    TestTimes.add()
    payload = json.dumps({
        'username': '',
        'id_card': 'A123456789',
        'date_of_birth': '2022-05-23',
        'mobile_number': '0987654321',
    })
    times = 1
    for i in range(times):
        r = requests.request('POST', RestPwdUrl, headers = JsonHeaders, data = payload)
        TestTimes2.add()
        time.sleep(100/1000)
    return HttpResponse(
            f'第{TestTimes.test_times}次惡作劇<br>\
            傳送了{TestTimes2.test_times}次<br>\
            結束時間為{datetime.now().strftime("%H:%M:%S")}<br>\
            耗時:{format(time.time() - start)}<br>\
            最終內容:<br>\
            {r.text}<br>\
            <br>\
            {r.content.decode("utf-8")}<br>\
            <br>\
            {r.headers}<br>\
            <br>\
            {r.headers.keys()}'
    ) #Content-Type


#igc2
def igc2(request):
    dic={
        'a': None,
        'b': ''
    }
    return HttpResponse(dic)

#igc3
class IGC3View(APIView):
    def get(self,request):
        return Response(CodeMessageEnum(640).to_dict())


#igc0
class IGC0View(APIView):
    def get(self, request):
        print('>-----------------------------------<')
        print(request.body)
        print('>-----------------------------------<')
        data0 = { #request的headers
            # 'keys':request.headers.keys(),
            'Content-Length': request.headers.get('Content-Length'),
            'Content-Type': request.headers.get('Content-Type'),
            'Host': request.headers.get('Host'),
            'Connection': request.headers.get('Connection'),
            #下面這個是啥?
            # 'Cache-Control':request.headers.get('Cache-Control'),
            'Upgrade-Insecure-Requests': request.headers.get('Upgrade-Insecure-Requests'),
            'User-Agent': request.headers.get('User-Agent'),
            'Accept': request.headers.get('Accept'),
            'Accept-Encoding': request.headers.get('Accept-Encoding'),
            'Accept-Language': request.headers.get('Accept-Language'),
            'Cookie': request.headers.get('Cookie'),
        }
        data1 = { #request other
            'session': request.session,
            'body': request.body, 
            'get_host': request.get_host(),
            'get_port': request.get_port(),
            'get_full_path': request.get_full_path(),
            'get_full_path_info': request.get_full_path_info(),
            'build_absolute_uri': request.build_absolute_uri(location = None),
            # 'site':request.site,
        }
        data2 = { #request user
            'user':str(request.user),
        }
        strr = request.headers.get('Cookie')
        start = strr.find('csrftoken') + 10
        data3 = { #csrf
            'csrf': strr[start: start + 64]
        }
        data4 = { #try accept
            'request.accepts("text/html")': request.accepts('text/html')
        }
        data5 = {
            'readlines': request.readlines(),
            '__iter__': request.__iter__(),
        }
        data0.update(data1)
        data0.update(data3)
        data0.update(data4)
        time0 = datetime.strptime('2020-02-20', '%Y-%m-%d')
        response0 = HttpResponse()
        response = HttpResponse(content = b'', content_type = None, status = 200, reason = None, charset = None, headers = None)
        response['food']='apple'
        response.set_cookie(key = 'key0', value = 'value0', max_age = 300, expires = time0, path = '/', domain = 'www.googl.com', secure = False, httponly = False, samesite = None)
        data6 = {
            'response0.__dict__': response0.__dict__,
            'response.__dict__': response.__dict__,
            # 'items()': response.items(),
        }
        # return response
        return Response(data0)