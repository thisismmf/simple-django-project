from django.test import TestCase
from users.models import User, OneTimeCode
from django.utils import timezone

class UserModelTests(TestCase):
    def test_create_user_without_mobile_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(mobile=None)

    def test_create_superuser_has_permissions(self):
        admin = User.objects.create_superuser(mobile='1234', password='pwd')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

class OneTimeCodeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile='5555')
        self.code = OneTimeCode.objects.create(user=self.user, code='000000')

    def test_str_representation(self):
        self.assertEqual(str(self.code), f"{self.user.mobile} - 000000")