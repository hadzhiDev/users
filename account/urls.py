from django.urls import path
from . import views
from .yasg import urlpatterns as url_doc


urlpatterns = [
    path('login/', views.LoginGenericAPIView.as_view()),
    path('register/', views.RegisterGenericAPIView.as_view()),
    path('send-reset-password-key/', views.SendResetPasswordKeyApiView.as_view()),
    path('reset-password/', views.ResetPasswordApiView.as_view()),
]

urlpatterns += url_doc