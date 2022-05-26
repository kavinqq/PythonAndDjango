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

from utils.constant import RestPwdUrl, JsonHeaders, UnlockUrl, ForgetUserNameUrl, CheckAccountUrl, indexHtml
from datetime import datetime

from .models import Staff
from .serializers import *
from global_settings.enums import *

# 新增員工
@method_decorator(login_required, name = 'post')
class NewStaffView(GenericAPIView):

    serializer_class = AddStaffSerializers

    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data = data)

        # 驗證資料
        if not serializer.is_valid(raise_exception = True):
            ddata = CodeMessageEnum.ADD_NEW_EMPLOYEE_FAILED.to_dict()
            ddata.update(dict(data = '', is_error = CodeMessageEnum.ADD_NEW_EMPLOYEE_FAILED.is_error()))
            return render(request, indexHtml, {
                        'data': ddata,
                        'iusers': Staff.objects.all()
            })

        data = serializer.validated_data
        user = Staff.objects.create(
            username = data.get('username'),
            password = data.get('password'),
            IdCard = data.get('IdCard'),
            phoneNumber = data.get('phoneNumber'),
            authority = data.get('authority'),
            can_reset_password = data.get('can_reset_password'),
            can_unlock = data.get('can_unlock'),
            can_search_username = data.get('can_search_username'),
            can_check_status = data.get('can_check_status'),
        )
        ddata = CodeMessageEnum.ADD_NEW_EMPLOYEE_SUCCESS.to_dict()
        ddata.update(dict(data = '', is_error = CodeMessageEnum.ADD_NEW_EMPLOYEE_FAILED.is_error()))
        return render(request,indexHtml,{
                    'data': ddata,
                    'iusers': Staff.objects.all()
        })


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
            res = CodeMessageEnum.VALIDATION_ERROR.to_dict()
            res.update(dict(data = serializer.error_messages, is_error = CodeMessageEnum.VALIDATION_ERROR.is_error()))
            return res
            # return {'show':True,'is_error':True,'code': 801,'message': '資料格式(待傳輸)驗證錯誤','data':serializer.error_messages}
        data = serializer.validated_data
        res = CodeMessageEnum.VALIDATION_SUCCESS.to_dict()
        res.update(dict(data = data, is_error = CodeMessageEnum.VALIDATION_SUCCESS.is_error()))
        return res
        # return {'show':False,'is_error':False,'code': 701,'message': '資料格式(待傳輸)驗證通過','data':data}

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
            res = CodeMessageEnum.CONNECT_TO_SSO_FAILED.to_dict()
            res.update(dict(data = response.text, is_error = CodeMessageEnum.CONNECT_TO_SSO_FAILED.is_error()))
            return res
            # return {'show':True,'is_error':True,'code': 802,'message': '連線SSO出問題','data':response.text}
        response = json.loads(response.text)
        result = RetrieveDataSerializers(data=response)

        if not result.is_valid():
            print(CodeMessageEnum.RECEIVE_DATA_VALID_FAILED.message)
            res = CodeMessageEnum.RECEIVE_DATA_VALID_FAILED.to_dict()
            res.update(dict(data = result.error_messages, is_error = CodeMessageEnum.RECEIVE_DATA_VALID_FAILED.is_error()))
            return res
            # return {'show':True,'is_error':True,'code': 803,'message': '資料格式(接收)驗證錯誤','data':result.error_messages}

        valid_result = result.validated_data
        res = {'code': valid_result['code'], 'message': valid_result['message'], 'data': valid_result['data'], 'is_error': False}
        return res
        # return {'show':True,'is_error':False,'code': valid_result['code'],'message': valid_result['message'],'data':valid_result['data']}

    def short_do(self, request, url_to_exe):
        data0 = self.serializer_before_sent(request)
        print(data0)
        if data0.get('is_error'):
            print('待傳資料 驗證錯誤')
            return data0
        else:
            data = self.sent_receive_serializer(data0.get('data'), url_to_exe)
            return data

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
            'iusers': Staff.objects.all()
        })


#解鎖
class UnlockView(ControlPostView):
    def post(self, request):
        return render(request, indexHtml, {
            'data': self.short_do(request, UnlockUrl),
            'iusers': Staff.objects.all()
        }) 


#查帳號
class ForgetUsernameView(ControlPostView):
    def post(self, request):
        return render(request, indexHtml, {
            'data': self.short_do(request, ForgetUserNameUrl),
            'iusers': Staff.objects.all()
        })


#查開戶
class CheckAccountView(ControlPostView):
    def post(self, request):
        return render(request, indexHtml, {
            'data': self.short_do(request, CheckAccountUrl),
            'iusers': Staff.objects.all()
        })
#重構end-----------------------


# 輸入登入資訊
def page_to_login(request):
    return render(request, 'login.html')


# 登入
class LoginView(APIView):

    def post(self, request):
        print('start login post')

        data = request.data
        serializers = StaffLoginSerializers(data = data)

        if not serializers.is_valid():
            print('登入資料格式錯誤')
            return HttpResponseRedirect('/serviceapp/input/')
        #     try:
        #         # 撈出對應名稱的資料
        #         DbData = Staff.objects.get(username = data['username'])
        #     except Exception as e:
        #         print('無效的使用者名稱')
        #         return HttpResponseRedirect('/serviceapp/input/')
        # else :
        #     print('登入資料格式錯誤')
        #     return HttpResponseRedirect('/serviceapp/input/')

        data = serializers.validated_data
        print('驗證帳密')
        user = authenticate(request, username = data.get('username'), password = data.get('password'))
        dbuser = Staff.objects.get(username = data.get('username'))
        print(f'check pwd = {dbuser.check_password(data.get("password"))}')
        
        if user:
            print('成功')
            login(request, user)
            return redirect('/serviceapp/index/')
        else:
            print('失敗')
            return HttpResponseRedirect('/serviceapp/input/')


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


#測試網頁
def Test3(request):
    return render(request,indexHtml,{})


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


#測試用 小def
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
            耗時:{format(time.time()-start)}<br>\
            最終內容:<br>\
            {r.text}<br>\
            <br>\
            {r.content.decode("utf-8")}<br>\
            <br>\
            {r.headers}<br>\
            <br>\
            {r.headers.keys()}'
    ) #Content-Type


#測試用 小def2
def igc2(request):
    print((type(CodeMessageEnum.UNEXCEPTED_ERROR.to_dict())))
    a = CodeMessageEnum.UNEXCEPTED_ERROR.to_dict()
    return HttpResponse(f'{CodeMessageEnum(a.get("code")).is_error()}')


#測試用小class
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