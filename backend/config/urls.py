from django.conf import settings, urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, include

from .routers import router

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'^api/', include(router.urls)),
]

if settings.ENABLE_API:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    urlpatterns += (
        re_path(r'^api/docs/', SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
        re_path(r'^api/schema/', SpectacularAPIView.as_view(), name="schema"),
    )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [re_path(r'^__debug__/', urls.include(debug_toolbar.urls))] + urlpatterns
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
