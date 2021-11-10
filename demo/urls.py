"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from rest_framework_nested import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from djongo_app.api_views import (
    AccountViewSet as DjongoAccountViewSet,
    ShortLinkViewSet as DjongoAccountShortLinkViewSet,
)
from djongo_app.views import short_link_redirect as djongo_short_link_redirect
from mongoengine_app.api_views import (
    AccountViewSet as MEAccountViewSet,
    AccountShortLinkViewSet as MEAccountShortLinkViewSet,
)
from mongoengine_app.views import short_link_redirect as mongoengine_short_link_redirect

# Init Swagger schema view
SchemaView = get_schema_view(
    openapi.Info(
        title='Your API name',
        default_version='v1',
        description='Your API description',
        terms_of_service='your terms of service url',
        contact=openapi.Contact(email='your contact email'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

# Init Djongo API routers
djongo_router = routers.SimpleRouter()
djongo_router.register(
    r'accounts',
    DjongoAccountViewSet,
    basename='account',
)
# Use DRF nested routers
djongo_links_router = routers.NestedSimpleRouter(
    djongo_router,
    r'accounts',
    lookup='account',
)
djongo_links_router.register(
    r'links',
    DjongoAccountShortLinkViewSet,
    basename='account-link',
)

# Init MongoEngine API routers
mongoengine_router = routers.SimpleRouter()
mongoengine_router.register(
    r'accounts',
    MEAccountViewSet,
    basename='account',
)
# Use DRF nested routers
mongoengine_links_router = routers.NestedSimpleRouter(
    mongoengine_router,
    r'accounts',
    lookup='account',
)
mongoengine_links_router.register(
    r'links',
    MEAccountShortLinkViewSet,
    basename='account-link',
)

# Declare urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),

    # Browsable API views
    path('api-auth/', include('rest_framework.urls')),

    # Swagger views
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        SchemaView.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        SchemaView.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        SchemaView.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),

    # Djongo API
    path('djongo-api/', include(djongo_router.urls)),
    path('djongo-api/', include(djongo_links_router.urls)),
    # Djongo redirect from short links
    # NOTE: Using a regex here to make it work with and without a trailing slash
    re_path(
        r'^d/(?P<pk>[^/.]+)/?$',
        djongo_short_link_redirect,
        name='short-link',
    ),

    # MongoEngine API
    path('mongoengine-api/', include(mongoengine_router.urls)),
    path('mongoengine-api/', include(mongoengine_links_router.urls)),
    # MongoEngine redirect from short links
    # NOTE: Using a regex here to make it work with and without a trailing slash
    re_path(
        r'^me/(?P<pk>[^/.]+)/?$',
        mongoengine_short_link_redirect,
        name='short-link',
    ),
]