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
    re_path(r'^guests/', include('guests.urls',namespace='guests')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^email_prev/',include('babtynoemail.urls',namespace='babtynoemail')),
    #wagtail
    re_path(r'cms/', include(wagtailadmin_urls)),
    re_path(r'documents/', include(wagtaildocs_urls)),
    # re_path(r'^', include(wagtail_urls)),
    #end wagtail
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
        re_path(r'^', include(wagtail_urls)),
)

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
