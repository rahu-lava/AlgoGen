from django.contrib import admin
from django.urls import path,include
import credentials.urls
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',include('credentials.urls')),
    path('Re_assume_admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
