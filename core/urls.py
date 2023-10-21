from django.urls import path
from django.contrib import admin
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include("user.urls"))
]
