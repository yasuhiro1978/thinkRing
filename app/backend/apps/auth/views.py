from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    """カスタムログインView"""
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {
                    'error': {
                        'code': 'AUTH_001',
                        'message': 'ユーザー名とパスワードが必要です',
                        'type': 'validation_error'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {
                    'error': {
                        'code': 'AUTH_004',
                        'message': 'ログイン情報が正しくありません',
                        'type': 'authentication_error'
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        response = Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_200_OK
        )
        
        # Refresh TokenをHttpOnly Cookieに設定
        response.set_cookie(
            'refresh_token',
            str(refresh),
            httponly=True,
            samesite='Lax',
            max_age=60 * 60 * 24 * 7  # 7日
        )
        
        return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """ログアウトView"""
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception:
        pass
    
    response = Response(
        {'message': 'ログアウトしました'},
        status=status.HTTP_200_OK
    )
    response.delete_cookie('refresh_token')
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info_view(request):
    """ユーザー情報取得View"""
    return Response({
        'id': str(request.user.id),
        'username': request.user.username,
        'email': request.user.email,
    })

