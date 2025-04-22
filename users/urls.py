from django.urls import path
# Import views from the current app (users)
from . import views

# Use URL names consistent with the tests
urlpatterns = [
    path('mobile/', views.MobileView.as_view(), name='mobileview'),
    path('verify-code/', views.CodeVerifyView.as_view(), name='verifycode'),
    path('complete-registration/', views.CompleteRegistrationView.as_view(), name='completeregistration'),
    path('login/', views.LoginView.as_view(), name='login'),
]
