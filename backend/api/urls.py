from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import health, SiteViewSet, VerificationViewSet, WorkflowStepViewSet

router = routers.DefaultRouter()
router.register(r'sites', SiteViewSet, basename='site')
router.register(r'verifications', VerificationViewSet, basename='verification')
router.register(r'workflow-steps', WorkflowStepViewSet, basename='workflowstep')

schema_view = get_schema_view(
    openapi.Info(
        title="Site Verification API",
        default_version='v1',
        description="API for managing sites, verifications, and workflow steps.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('health/', health, name='Health'),
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
