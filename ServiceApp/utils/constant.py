from enum import Enum

class ServiceResponse(Enum):

    success = 0
    noData = 1
    fail = 2

# request json header
JsonHeaders = {'Content-Type': 'application/json'}

# SSO API URL
SSOIP =  'http://10.66.200.52:9487/'

RestPwdUrl = SSOIP + 'app1/resetpwd/'

ForgetUserNameUrl = SSOIP + 'app1/forgetusername/'

CheckAccountUrl = SSOIP + 'app1/checkaccount/'

UnlockUrl = SSOIP + 'app1/unlock/'

