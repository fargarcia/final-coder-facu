from django import views
from django.contrib import admin
from django.urls import path, include
from PrimeraEntregaFinalApp import views
from PrimeraEntregaFinalApp.views import inicio
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('admin/', admin.site.urls),
    path('PrimeraEntregaFinalApp/', include('PrimeraEntregaFinalApp.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)