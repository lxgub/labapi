from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # enables reset_password, you can see reset email in logs
    path('', include('django.contrib.auth.urls')),
    path('lab/', include('labapi.urls', namespace='labapi')),
]