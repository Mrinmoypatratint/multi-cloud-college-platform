from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import (
    CustomTokenObtainPairView, CurrentUserView, UserViewSet,
    StudentProfileViewSet, FacultyProfileViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('students', StudentProfileViewSet, basename='student')
router.register('faculties', FacultyProfileViewSet, basename='faculty')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('', include(router.urls)),
]
