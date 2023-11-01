"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# provide a view for the swagger api doc
schema_view = get_schema_view(
    openapi.Info(
        title="Projects API",
        default_version="v1",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="andrew.burton@ucalgary.ca"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # api urls
    path('', include('api.urls', namespace='apis')),
    # authentication urls
    path('users/', include('users.urls', namespace='users')),
    # rest framework api (might remove later)
    path('apis-auth/', include('rest_framework.urls')),
    # admin panel access (will be replaced with a custom admin panel)
    path('admin/', admin.site.urls),
    # documented api route
    path('schemas/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# include media roots if in debug mode (other environments will provide media files from a web server like nginx/apache)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
