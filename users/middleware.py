from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from datetime import timedelta

class IPBlockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if cache.get(f"blocked_{ip}"):
            return JsonResponse({ 'detail': 'Too many attempts. Try again later.' }, status=429)