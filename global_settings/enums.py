from enum import Enum

IS_ERROR = True

class CodeMessageEnum(Enum):
    '''
    狀態碼 訊息 is_error
    '''    
    UNEXCEPTED_ERROR = (800, '不可預期錯誤', IS_ERROR)

    RESET_PASSWORD_SUCCESS = (702, '重置密碼成功', not IS_ERROR)
    RESET_PASSWORD_FAILED =  (802, '重置密碼失敗', IS_ERROR)

    UNLOCK_SUCCESS = (703, '解鎖成功', not IS_ERROR)
    UNLOCK_FAILED =  (803, '解鎖失敗', IS_ERROR)

    SERACH_USERNAME_SUCCESS = (704, '查詢帳號成功', not IS_ERROR)
    SERACH_USERNAME_FAILED =  (804, '查詢帳號失敗', IS_ERROR)

    CHECK_STATUS_SUCCESS = (705, '查看狀態成功', not IS_ERROR)
    CHECK_STATUS_FAILED =  (805, '查看狀態失敗', IS_ERROR)

    ADD_NEW_EMPLOYEE_SUCCESS = (706, '新增員工成功', not IS_ERROR)
    ADD_NEW_EMPLOYEE_FAILED =  (806, '新增員工失敗', IS_ERROR)

    CHANGE_PERMISSION_SUCCESS = (707, '改變權限成功', not IS_ERROR)
    CHANGE_PERMISSION_FAILED =  (807, '改變權限失敗', IS_ERROR)

    VALIDATION_SUCCESS = (708, '驗證成功', not IS_ERROR)
    VALIDATION_FAILED =  (808, '驗證失敗', IS_ERROR)

    CONNECT_TO_SSO_SUCCESS = (709, '連線SSO成功', not IS_ERROR)
    CONNECT_TO_SSO_FAILED =  (809, '連線SSO失敗', IS_ERROR)

    RECEIVE_DATA_VALID_SUCCESS = (710, '回傳資料驗證成功', not IS_ERROR)
    RECEIVE_DATA_VALID_FAILED =  (810, '回傳資料驗證失敗', IS_ERROR)

    LOGIN_SUCCESS = (711, '登入成功', not IS_ERROR)
    LOGIN_FAILED =  (811, '登入失敗', IS_ERROR)

    LOGOUT_SUCCESS = (712, '登出成功', not IS_ERROR)
    LOGOUT_FAILED =  (812, '登出失敗', IS_ERROR)

    def __new__(cls, code, message, is_error):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.code = code
        obj.message = message
        obj.is_error = is_error
        return obj
    
    def to_dict(self,data=None) -> dict:        
        return dict(code = self.code, message = self.message, is_error = self.is_error, data = data)

    @classmethod
    def _missing_(cls,value:str):
        return CodeMessageEnum.UNEXCEPTED_ERROR