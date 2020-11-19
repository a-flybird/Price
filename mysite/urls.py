from django.conf.urls import url
from django.contrib import admin
from django.urls import include

urlpatterns = [
    url('admin/', admin.site.urls),
#    path('loginpage/', include('myapp.urls')),
    url('/',include('myapp.urls',namespace='api'),),
]

