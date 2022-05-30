from ServiceApp.models import *

# request json header
JSON_HEADERS = {'Content-Type': 'application/json'}

# SSO API URL
SSO_IP =  'http://10.66.200.53:8000/'

# RestPwdUrl = SSOIP + 'app1/resetpwd/'
# UnlockUrl = SSOIP + 'app1/unlock/'
# ForgetUserNameUrl = SSOIP + 'app1/forgetusername/'
# CheckAccountUrl = SSOIP + 'app1/checkaccount/'

def get_sso_url(key):
    '''
    取得連線到sso的url
    '''
    data = {
        'reset_pwd': 'app1/resetpwd/',
        'unlock': 'app1/unlock/',
        'find_username': 'app1/forgetusername/',
        'check_account': 'app1/checkaccount/',
    }
    return SSO_IP + data.get(key)

INDEX_HTML = 'test3.html'


class get_users(object):
    '''
    依照不同發法取得其他的員工資料
    '''

    def gt(user):
        '''
        取得的其他員工 權限數字比該使用者 大
        '''
        return Staff.objects.filter(authority__gt = user.authority)

    def gte(user):
        '''
        取得的其他員工 權限數字比該使用者 大.相等
        '''
        return Staff.objects.filter(authority__gte = user.authority)

    def lt(user):
        '''
        取得的其他員工 權限數字比該使用者 小
        '''
        return Staff.objects.filter(authority__lt = user.authority)

    def lte(user):
        '''
        取得的其他員工 權限數字比該使用者 小.相等
        '''
        return Staff.objects.filter(authority__lte = user.authority)
    
    def all():
        '''
        回傳全部員工
        '''
        return Staff.objects.all()