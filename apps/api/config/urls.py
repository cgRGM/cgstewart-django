"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from datetime import datetime

# Simple health check view for Vercel
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django API is running on Vercel!',
        'timestamp': datetime.now().isoformat(),
        'database': 'neon-serverless'
    })

urlpatterns = [
    path('', health_check, name='health_check'),  # Root endpoint for Vercel
    path('admin/', admin.site.urls),
    path('api/v1/', include('blog.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
