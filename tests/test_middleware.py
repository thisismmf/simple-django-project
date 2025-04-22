from django.test import TestCase, RequestFactory
from users.middleware import IPBlockMiddleware
from django.core.cache import cache

class MiddlewareTests(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        self.middleware = IPBlockMiddleware()

    def test_ip_blocking(self):
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '1.2.3.4'
        cache.set('blocked_1.2.3.4', True, timeout=3600)
        response = self.middleware.process_request(request)
        self.assertEqual(response.status_code, 429)