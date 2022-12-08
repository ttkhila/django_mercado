from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mercado/', include('mercado.urls')),
    path('', include('mercado.urls'))
]
