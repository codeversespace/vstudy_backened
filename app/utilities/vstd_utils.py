class GetCode:
    def subject(self, sub_str: str = None):
        if sub_str == 'computer':
            return 29
        if sub_str == 'hindi':
            return 28
        else :
            return 11

    def subjectById(self, sub_str: str = None):
        if sub_str == '29':
            return 'computer'
        if sub_str == '28':
            return 'hindi'
        else :
            return 'common'


getCode = GetCode()


