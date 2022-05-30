from enum import Enum

from ServiceApp.models import *

class ServiceResponse(Enum):

    success = 0
    noData = 1
    fail = 2

# request json header
JsonHeaders = {'Content-Type': 'application/json'}

# SSO API URL
SSOIP =  'http://10.66.200.53:8000/'

RestPwdUrl = SSOIP + 'app1/resetpwd/'

UnlockUrl = SSOIP + 'app1/unlock/'

ForgetUserNameUrl = SSOIP + 'app1/forgetusername/'

CheckAccountUrl = SSOIP + 'app1/checkaccount/'

indexHtml = 'test3.html'

def get_url(key):
    data = {
        'RestPwdUrl': 'app1/resetpwd/',
        'UnlockUrl': 'app1/unlock/',
        'ForgetUserNameUrl': 'app1/forgetusername/',
        'CheckAccountUrl': 'app1/checkaccount/',
    }

    return SSOIP + data.get(key)


class get_users(object):
    def gt(self,user):
        return Staff.objects.filter(authority__gt = user.authority)

    def gte(self,user):
        return Staff.objects.filter(authority__gte = user.authority)

    def lt(self,user):
        return Staff.objects.filter(authority__lt = user.authority)

    def lte(self,user):
        return Staff.objects.filter(authority__lte = user.authority)