import random
import re
import string
import uuid
from typing import List
from uuid import UUID


class NeStrings:
    @staticmethod
    def isEmpty(val: str):
        if val is None:
            return True
        if isinstance(val, str) and len(val.strip()) == 0:
            return True
        return False

    @staticmethod
    def isNotEmpty(val: str):
        return not NeStrings.isEmpty(val)

    @staticmethod
    def nullToNone(src: str):
        if NeStrings.isNotEmpty(src) and src.lower() == "null":
            return None
        return src

    @staticmethod
    def defaultIfEmpty(val: str, default_val: str = ''):
        if NeStrings.isEmpty(val):
            return default_val
        return val

    @staticmethod
    def emptyToNone(val: str):
        if NeStrings.isEmpty(val):
            return None
        return val

    @staticmethod
    def toString(val: bool) -> str:
        return str(val)

    @staticmethod
    def toLower(val: str) -> str:
        if val is None:
            return val
        return str(val).lower()

    @staticmethod
    def toUpper(val: str) -> str:
        if val is None:
            return val
        return str(val).upper()

    @staticmethod
    def uuidv4() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def isValidUuid(uuid_to_test, version=4):
        """
        Check if uuid_to_test is a valid UUID.
         Parameters
        ----------
        uuid_to_test : str
        version : {1, 2, 3, 4}
         Returns
        -------
        `True` if uuid_to_test is a valid UUID, otherwise `False`.

         Examples
        --------
        >>> isValidUuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
        True
        >>> isValidUuid('c9bf9e58')
        False
        """

        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    @staticmethod
    def removeNonAlphanum(val: str):
        if val is None:
            return val
        out = ''.join(e for e in val if e.isalnum())
        return out

    @staticmethod
    def removeSpecialCharsNotSpaces(val: str):
        if val is None:
            return val
        out = re.sub("[^A-Za-z0-9 ]", "", val)
        return out

    @staticmethod
    def randomAlphaNumeric(length: int = 5):
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=length))
        return res

    @staticmethod
    def containsIgnoreCaseAnyOf(src: str, strs_to_find: List[str]):
        if strs_to_find is None or len(strs_to_find) == 0:
            raise Exception(f'Nothing provided to find in source string {src}')
        if NeStrings.isEmpty(src):
            raise Exception(f"No source string provided where to find {strs_to_find}")
        src_lower = src.lower()
        for stf in strs_to_find:
            if stf is None:
                continue
            if stf.lower() in src_lower:
                return True
        return False

    @staticmethod
    def containsIgnoreCase(src: str, str_to_find: str):
        if NeStrings.isEmpty(str_to_find):
            raise Exception(f'Nothing provided to find in source string {src}')
        if NeStrings.isEmpty(src):
            raise Exception(f"No source string provided where to find {str_to_find}")
        src_lower = src.lower()
        return str_to_find.lower() in src_lower

    @staticmethod
    def equalsIgnoreCase(src: str, str_to_find: str):
        if NeStrings.isEmpty(str_to_find):
            raise Exception(f'Nothing provided to find in source string {src}')
        if NeStrings.isEmpty(src):
            raise Exception(f"No source string provided where to find {str_to_find}")
        src_lower = src.lower()
        if str_to_find.lower() == src_lower:
            return True
        return False

    @staticmethod
    def extractDefaultToNone(src: str, regex, group_no: int = 0):
        try:
            output = re.search(regex, src).group(group_no)
        except:
            output = None
        return output

    @staticmethod
    def repeatChar(char_to_repeat: str = "-", times: int = 80):
        if times is None or times < 0:
            times = 80
        result = ""
        for i in range(times):
            result = result + char_to_repeat
        return result
