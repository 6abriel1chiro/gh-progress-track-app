from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from journal_api.views import register_user, JournalEntryViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Coding Journal API",
        default_version="v1",
        description="API for tracking daily coding activities and learnings",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Router for viewsets
router = DefaultRouter()
router.register(r"entries", JournalEntryViewSet, basename="entry")

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API Documentation
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # API Endpoints
    path("api/", include(router.urls)),
    path("api/register/", register_user, name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
