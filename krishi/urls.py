from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import SignupViewSet, VetRequestViewSet, AboutUsViewSet, PasswordResetViewSet

router = DefaultRouter()
router.register('signup', SignupViewSet, basename='signup')
router.register('vetrequest', VetRequestViewSet, basename='vetrequest')
router.register('aboutus', AboutUsViewSet, basename='aboutus')
router.register('passwordreset', PasswordResetViewSet, basename='passwordreset')

urlpatterns = [
    path('api/', include(router.urls)),

    # LOGIN
    path('api/login/', TokenObtainPairView.as_view(), name="login"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
