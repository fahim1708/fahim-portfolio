from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Content Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("projects/", include("apps.projects.urls")),
    path("research/", include("apps.research.urls")),
    path("", include("apps.core.urls")),
]

handler404 = "apps.core.views.page_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
