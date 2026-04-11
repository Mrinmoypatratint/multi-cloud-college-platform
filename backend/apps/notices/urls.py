from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.notices.views import NoticeViewSet

router = DefaultRouter()
router.register('', NoticeViewSet, basename='notice')

urlpatterns = [
    path('', include(router.urls)),
]
