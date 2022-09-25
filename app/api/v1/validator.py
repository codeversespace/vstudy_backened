from app.utilities.response import returnResponse
from configurations.role_definer import RoleAuthenticator
responseHandler = returnResponse()

def if_request_valid(role_level,user_id):
    if role_level.lower() == 'super':
        if str(user_id) not in RoleAuthenticator.SuperRole.role_list:
            return False
        return True
