from django.contrib import admin
from django.urls import path, include
from items.views import get_user_info
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ReviveIt API",
        default_version='v1',
        description="API documentation for ReviveIt",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('items.urls')),
    path('api/user/', get_user_info, name='get_user_info'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]