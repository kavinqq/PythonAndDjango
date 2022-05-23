from django.urls import path
from .views import NewStaff,RestPasswordView,UnlockView,CheckAccountView,ForgetUsernameView,Test,Login,inputAccountInfo,TestAuth

urlpatterns = [ 
    path('test/',Test),    
    path('newStaff/',NewStaff.as_view()),
    path('input/', inputAccountInfo.as_view(), name="input"),
    path('login/', Login.as_view(), name="login"),
    path('TestAuth/', TestAuth),

    #SSO API
    path('ResetPassword/',RestPasswordView.as_view()),
    path('Unlock/',UnlockView.as_view(), name = "unlock"),
    path('ForgetUsername/',ForgetUsernameView.as_view()),
    path('CheckAccount/',CheckAccountView.as_view()),
]