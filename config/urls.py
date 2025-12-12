from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # Importe o RedirectView

urlpatterns = [
    # Redireciona a URL raiz ('') diretamente para '/login/'
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='home'), 
    
    path('admin/', admin.site.urls),
    path('', include('nutrix.urls')),
]