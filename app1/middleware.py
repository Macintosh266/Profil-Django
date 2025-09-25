from django.http import JsonResponse, Http404
from django.urls import resolve, Resolver404
import logging
import json

logger = logging.getLogger(__name__)

class APIErrorHandlingMiddleware:
    """
    API so'rovlari uchun xatolarni boshqarish middleware'i
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Exception'larni qayta ishlash
        """
        # Faqat API so'rovlari uchun
        if not self.is_api_request(request):
            return None

        # 404 xatolar uchun
        if isinstance(exception, (Http404, Resolver404)):
            logger.warning(f"API 404 error: {request.path} from IP: {self.get_client_ip(request)}")
            return JsonResponse({
                'success': False,
                'error': 'Not Found',
                'message': 'The requested API endpoint was not found.',
                'status_code': 404
            }, status=404)

        # Boshqa xatolar uchun
        logger.error(f"API server error: {str(exception)} at {request.path} from IP: {self.get_client_ip(request)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An error occurred while processing your request.',
            'status_code': 500
        }, status=500)

    def process_response(self, request, response):
        """
        Response'larni qayta ishlash
        """
        # API so'rovlari uchun 404 response'larni o'zgartirish
        if self.is_api_request(request) and response.status_code == 404:
            logger.warning(f"API 404 response: {request.path} from IP: {self.get_client_ip(request)}")
            return JsonResponse({
                'success': False,
                'error': 'Not Found',
                'message': 'The requested API endpoint was not found.',
                'status_code': 404
            }, status=404)

        return response

    def is_api_request(self, request):
        """
        So'rov API so'rovi ekanligini tekshirish
        """
        api_patterns = ['/api/', '/rest/', '/v1/', '/v2/']  # API pattern'laringizni qo'shing
        return any(request.path.startswith(pattern) for pattern in api_patterns)

    def get_client_ip(self, request):
        """
        Foydalanuvchi IP manzilini olish
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware:
    """
    Xavfsizlik header'larini qo'shish
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # API response'lari uchun maxsus header'lar
        if request.path.startswith('/api/'):
            response['Content-Type'] = 'application/json'
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
            
        return response