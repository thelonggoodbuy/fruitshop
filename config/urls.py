from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("fruitshop_app/", include("fruitshop_app.urls"))
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
