from django.urls import re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    #re_path(r'^', include('wedding.urls')),
    re_path(r'^guests/', include('guests.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path('^accounts/', include('django.contrib.auth.urls')),
    #wagtail
    re_path('cms/', include(wagtailadmin_urls)),
    re_path('documents/', include(wagtaildocs_urls)),
    re_path('^', include(wagtail_urls)),
    #end wagtail
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
