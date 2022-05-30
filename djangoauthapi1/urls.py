from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


def home(request):
    return HttpResponse("hello")


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('account.urls'))
]
