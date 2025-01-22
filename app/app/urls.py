from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
import app.settings as settings
import main.urls as main_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(main_urls.urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
