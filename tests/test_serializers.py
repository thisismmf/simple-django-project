from django.test import TestCase
from users.serializers import MobileSerializer, PasswordSerializer, CodeVerifySerializer, RegistrationSerializer

class SerializerValidationTests(TestCase):
    def test_mobile_serializer_valid(self):
        data = {'mobile': '12345'}
        serializer = MobileSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_serializer_missing(self):
        serializer = PasswordSerializer(data={'mobile': '123'})
        self.assertFalse(serializer.is_valid())

    def test_registration_serializer_requires_fields(self):
        serializer = RegistrationSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('mobile', serializer.errors)