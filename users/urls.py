from django.urls import path
from .views import MobileView, CodeVerifyView, CompleteRegistrationView, LoginView

urlpatterns = [
    path('mobile/', MobileView.as_view()),
    path('verify-code/', CodeVerifyView.as_view()),
    path('complete-registration/', CompleteRegistrationView.as_view()),
    path('login/', LoginView.as_view()),
]