from django.urls import path
from drf_spectacular.views import (SpectacularAPIView,
                                    SpectacularRedocView,
                                    SpectacularSwaggerView)
from django.conf import settings

all_apps = settings.INSTALLED_APPS

class DynamicDRFSpectacular:
    def __init__(self,installed_apps):
        self.installed_apps:list = installed_apps
        self.urlpatterns = []

    def override_apps(self) -> list:
        self.installed_apps.append("drf_spectacular")
        return self.installed_apps
    
    def append_urls(self) -> list:
        self.urlpatterns+=[
                path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                path('api/schema/redoc/',SpectacularRedocView.as_view(url_name='schema'), name='redoc'),]
        return self.urlpatterns

        

spectacular= DynamicDRFSpectacular(all_apps)
installed_apps = spectacular.override_apps()
urlpatterns = spectacular.append_urls()

    