"""
URL configuration for eccomerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
# from main.views import UserViewSet

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path("shop/",include("shop.urls")),
    path("blog/",include("blog.urls")),
    path("",views.index,name="index"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#this is also for image inserting
