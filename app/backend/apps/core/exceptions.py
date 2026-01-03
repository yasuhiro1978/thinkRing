from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """カスタム例外ハンドラー"""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': {
                'code': getattr(exc, 'default_code', 'SRV_001'),
                'message': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
                'type': exc.__class__.__name__,
                'timestamp': timezone.now().isoformat(),
            }
        }
        response.data = custom_response_data
        
        # ログ記録
        logger.error(
            f"Error: {exc.__class__.__name__} - {exc.detail if hasattr(exc, 'detail') else str(exc)}",
            extra={'context': context}
        )
    
    return response

