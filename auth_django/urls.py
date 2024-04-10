from django.contrib import admin
from django.urls import path, include
from auth_app.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('', home, name='home'),
]
