"""crossingpaths URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from crossingpathsapi.views.flosscolor import FlossColors
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from crossingpathsapi.views import register_user, login_user
from crossingpathsapi.views import Categories, CrossingUsers, Designs, Follows, CurrentUser

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'currentuser', CurrentUser, 'crossinguser')
router.register(r'users', CrossingUsers, 'crossinguser')
router.register(r'designs', Designs, 'design')
router.register(r'follows', Follows, 'follow')
router.register(r'colors', FlossColors, 'colors')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
