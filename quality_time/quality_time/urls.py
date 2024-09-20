"""
URL configuration for quality_time project.

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
from django.urls import path
from django.conf.urls import include
from activities.urls import router as activities_router

from django.conf import settings # New
from django.contrib.staticfiles.urls import static # New
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # New

#from rest_framework import routers


#router = routers.DefaultRouter()
#router.register(r'Activity', views.ActivityViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("activities.urls")),
#    path('api/Activity/bulk/', include("activities.urls")),
#    path('api/', include(activities_router.urls)),
#    path('api/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += staticfiles_urlpatterns() # New
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # New
