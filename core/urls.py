from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as url_doc

router = DefaultRouter()
router.register('posts', views.PostViewSet)

urlpatterns = [
    path('auth/', include('account.urls')),

    path('', include(router.urls))
]

urlpatterns += url_doc