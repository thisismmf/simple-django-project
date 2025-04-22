from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User, OneTimeCode
from django.core.cache import cache

class AuthFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        cache.clear()

    def test_registration_and_verification_flow(self):
        url_mobile = reverse('mobileview')
        url_verify = reverse('verifycode')
        url_complete = reverse('completeregistration')
        # request code
        resp = self.client.post('/api/auth/mobile/', {'mobile': '9999'}, format='json')
        self.assertEqual(resp.status_code, 201)
        user = User.objects.get(mobile='9999')
        otp = OneTimeCode.objects.filter(user=user).latest('created_at')

        # wrong code
        resp = self.client.post('/api/auth/verify-code/', {'mobile': '9999', 'code': 'wrong'}, format='json')
        self.assertEqual(resp.status_code, 400)

        # correct code
        resp = self.client.post('/api/auth/verify-code/', {'mobile': '9999', 'code': otp.code}, format='json')
        self.assertEqual(resp.status_code, 200)

        # complete registration
        resp = self.client.post('/api/auth/complete-registration/', {
            'mobile': '9999', 'full_name': 'Test', 'email': 't@example.com', 'password': 'aaa'
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.check_password('aaa'))

    def test_login_block_after_three_failures(self):
        User.objects.create_user(mobile='1111', password='pass')
        for i in range(3):
            resp = self.client.post('/api/auth/login/', {'mobile': '1111', 'password': 'wrong'}, format='json')
        self.assertEqual(resp.status_code, 429)