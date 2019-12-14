"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # you shouldn't do this in Django: from . import settings

# static.static(): Helper function to return a URL pattern for serving files in debug mode
from django.conf.urls.static import static

# for testing Sentry
# def trigger_error(request):
#     division_by_zero = 1 / 0


# You shouldn't change this variable name 'urlpatterns'
# urlpatterns = [path("admin/", admin.site.urls)]
urlpatterns = [
    # path("", include("core.urls", namespace="core")),
    # path("rooms/", include("rooms.urls", namespace="rooms")),
    path("", include("core.urls", namespace="core")),
    # TODO: "admin/" - this is not secure.
    #   Use EB evironment property for admin path
    #   or generate random path whenever it's deployed
    path(os.environ.get("DJANGO_ADMIN_PATH", "admin/"), admin.site.urls),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("users/", include("users.urls", namespace="users")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path("reviews/", include("reviews.urls", namespace="reviews")),
    path("lists/", include("lists.urls", namespace="lists")),
    path("conversations/", include("conversations.urls", namespace="conversations")),
    # path("sentry-debug/", trigger_error),  # for testing Sentry
]


# Serving files uploaded by a user during development
"""
    During development, you can serve user-uploaded media files from MEDIA_ROOT using the django.views.static.serve() view.
    This is not suitable for production use! For some common deployment strategies, see Deploying static files.
    For some common deployment strategies, see https://docs.djangoproject.com/en/2.2/howto/static-files/deployment/
"""
if settings.DEBUG:  # for debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:  # for release mode
    pass
