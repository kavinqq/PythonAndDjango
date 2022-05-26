from enum import Enum

class CodeMessageEnum(bytes, Enum):
    '''
    狀態碼 訊息 組合
    7XX 成功
    8XX 失敗
    '''
    UNEXCEPTED_ERROR = (888, '不可預期錯誤')

    LOGIN_SUCCESS = (700, '登入成功')
    LOGIN_FAILED =  (800, '登入失敗')

    LOGOUT_SUCCESS = (701, '登出成功')
    LOGOUT_FAILED =  (801, '登出失敗')

    RESET_PASSWORD_SUCCESS = (702, '重置密碼成功')
    RESET_PASSWORD_FAILED =  (802, '重置密碼失敗')

    UNLOCK_SUCCESS = (703, '解鎖成功')
    UNLOCK_FAILED =  (803, '解鎖失敗')

    SERACH_USERNAME_SUCCESS = (704, '查詢帳號成功')
    SERACH_USERNAME_FAILED =  (804, '查詢帳號失敗')

    CHECK_STATUS_SUCCESS = (705, '查看狀態成功')
    CHECK_STATUS_FAILED =  (805, '查看狀態失敗')

    ADD_NEW_EMPLOYEE_SUCCESS = (706, '新增員工成功')
    ADD_NEW_EMPLOYEE_FAILED =  (806, '新增員工失敗')

    CHANGE_PERMISSION_SUCCESS = (707, '改變權限成功')
    CHANGE_PERMISSION_FAILED =  (807, '改變權限失敗')

    VALIDATION_SUCCESS = (708, '驗證成功')
    VALIDATION_FAILED =  (808, '驗證失敗')

    CONNECT_TO_SSO_SUCCESS = (709, '連線SSO成功')
    CONNECT_TO_SSO_FAILED =  (809, '連線SSO失敗')

    RECEIVE_DATA_VALID_SUCCESS = (710, '回傳資料驗證成功')
    RECEIVE_DATA_VALID_FAILED =  (810, '回傳資料驗證失敗')

    def __new__(cls, code = 777, message = '驚不驚喜 意不意外'):
        obj = bytes.__new__(cls, code)
        obj._value_ = code
        obj.code = code
        obj.message = message
        return obj
    
    def to_dict(self) -> dict:        
        return dict(code = self.code, message = self.message)

    def is_error(self) -> bool:
        return (self.code / 100) == 8