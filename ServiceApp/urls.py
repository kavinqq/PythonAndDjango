from django.urls import path
from .views import *

urlpatterns = [ 
    #新增會員  
    path('newstaff/',NewStaffView.as_view(),name='newStaff'),
    #登入頁面
    path('input/', inputAccountInfo, name="input"),
    #處理登入帳密的功能，登入成功與否都會跳轉
    path('login/', LoginView.as_view(), name="login"),
    #登出功能
    path('logout/',logout_user,name='logout'),
    #預設的頁面
    path('index/', TestAuth),
    #主管修改組員權限
    path('change/',ChangePermissionView.as_view(),name='change'),
    #igc專用
    path('igc/',IGCView.as_view(),name='igc'),
    #SSO API:重置密碼
    path('resetpwd/',RestPasswordView.as_view(), name ="resetpwd"),
    #SSO API:解鎖
    path('unlock/',UnlockView.as_view(), name = "unlock"),
    #SSO API:忘記帳號
    path('forgetusername/',ForgetUsernameView.as_view(), name ="forgetusername"),
    #SSO API:查看帳戶
    path('checkaccount/',CheckAccountView.as_view(), name ="checkaccount"),
    #test
    path('test/',Test), 
    path('test3/',Test3),
    path('igc0/',IGC0View.as_view()),
    path('igc1/',igc1),
]