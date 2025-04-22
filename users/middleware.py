from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from datetime import timedelta

class IPBlockMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        # allow instantiation with no args (tests) but still work in real Django
        self.get_response = get_response
        if get_response is not None:
            super().__init__(get_response)
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if cache.get(f"blocked_{ip}"):
            return JsonResponse({ 'detail': 'Too many attempts. Try again later.' }, status=429)