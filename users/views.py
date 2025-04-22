import random
from django.utils import timezone
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, OneTimeCode
from .serializers import (
    MobileSerializer, PasswordSerializer,
    CodeVerifySerializer, RegistrationSerializer
)

def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')

class MobileView(APIView):
    def post(self, request):
        serializer = MobileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        ip = get_client_ip(request)

        user = User.objects.filter(mobile=mobile).first()
        if user:
            return Response({ 'registered': True }, status=200)

        # track registration attempts
        key = f"reg_fail_{ip}"
        nums = cache.get(key, set())
        nums.add(mobile)
        cache.set(key, nums, timeout=3600)
        if len(nums) >= 3:
            cache.set(f"blocked_{ip}", True, timeout=3600)
            return Response({ 'detail': 'Too many registration attempts.' }, status=429)

        # create user and code
        user = User.objects.create_user(mobile=mobile)
        code = f"{random.randint(100000,999999)}"
        OneTimeCode.objects.create(user=user, code=code)
        # Here you would send SMS
        return Response({ 'detail': 'Verification code sent.' }, status=201)

class CodeVerifyView(APIView):
    def post(self, request):
        serializer = CodeVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        code = serializer.validated_data['code']
        user = User.objects.filter(mobile=mobile).first()
        if not user:
            return Response({ 'detail': 'User not found.' }, status=404)

        otp = OneTimeCode.objects.filter(user=user).order_by('-created_at').first()
        if otp and otp.code == code and (timezone.now() - otp.created_at).seconds < 300:
            cache.delete(f"reg_fail_{get_client_ip(request)}")
            return Response({ 'detail': 'Code verified. Proceed to registration.' })

        return Response({ 'detail': 'Invalid code.' }, status=400)

class CompleteRegistrationView(APIView):
    def post(self, request):
        # Get mobile from request data directly
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'detail': 'Mobile number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Pass the user instance to the serializer to update it
        serializer = RegistrationSerializer(user, data=request.data, partial=True) # Use partial=True if needed
        serializer.is_valid(raise_exception=True)

        user.full_name = serializer.validated_data['full_name']
        user.email = serializer.validated_data['email']
        # Set password using the validated data
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({ 'detail': 'Registration complete.' })

class LoginView(APIView):
    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        password = serializer.validated_data['password']
        ip = get_client_ip(request)

        user = User.objects.filter(mobile=mobile).first()
        if not user or not user.check_password(password):
            key = f"login_fail_{ip}"
            count = cache.get(key, 0) + 1
            cache.set(key, count, timeout=3600)
            # block on third failure
            if count >= 3:
                cache.set(f"blocked_{ip}", True, timeout=3600)
                return Response({ 'detail': 'Invalid credentials.' }, status=429)
            return Response({ 'detail': 'Invalid credentials.' }, status=400)

        cache.delete(f"login_fail_{ip}")
        return Response({ 'detail': 'Login successful.' })