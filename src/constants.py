class MESSAGES:
    OK_CODE = 100
    INCORRECT_NAMESPACE_CODE = 202
    INCORRECT_TYPE_CODE = 207
    INCORRECT_GUARD_CODE = 205
    INCORRECT_KEY_CODE = 203

    OK = {"code": OK_CODE, "description": "OK"}
    INCORRECT_NAMESPACE = {"code": INCORRECT_NAMESPACE_CODE, "description": "Incorrect (nonexisting) namespace"}
    INCORRECT_TYPE = {"code": INCORRECT_TYPE_CODE, "description": "Incorrect type"}
    INCORRECT_GUARD = {"code": INCORRECT_GUARD_CODE, "description": "Incorrect guard"}
    INCORRECT_KEY = {"code": INCORRECT_KEY_CODE, "description": "Incorrect key"}

    USER_ALREADY_EXISTS_CODE = 201
    USER_CREATED_CODE = 200
    USER_NOT_FOUND_CODE = 204
    USER_UPDATED_CODE = 200
    USER_DELETED_CODE = 200

    USER_ALREADY_EXISTS = {"code": USER_ALREADY_EXISTS_CODE, "description": "User already exists"}
    USER_CREATED = {"code": USER_CREATED_CODE, "description": "User created"}
    USER_NOT_FOUND = {"code": USER_NOT_FOUND_CODE, "description": "User not found"}
    USER_UPDATED = {"code": USER_UPDATED_CODE, "description": "User updated"}
    USER_DELETED = {"code": USER_DELETED_CODE, "description": "User deleted"}

    @classmethod
    def ok(cls, value, guard):
        result = cls.OK.copy()
        result['value'] = value
        result['guard'] = guard
        return result
