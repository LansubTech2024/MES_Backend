from django.urls import path
from .views import SignUpView, SignInView, LogoutView, UpdateProfileView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]