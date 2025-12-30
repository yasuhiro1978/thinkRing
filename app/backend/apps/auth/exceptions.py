from rest_framework.exceptions import APIException
from rest_framework import status


class AuthenticationError(APIException):
    """認証エラー"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '認証が必要です'
    default_code = 'AUTH_001'


class ValidationError(APIException):
    """バリデーションエラー"""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'バリデーションエラーが発生しました'
    default_code = 'VAL_001'


class ResourceNotFoundError(APIException):
    """リソースが見つからないエラー"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'リソースが見つかりません'
    default_code = 'RES_001'

