
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from persons.views import showHome
from accounts.views import login_view,logout_view
urlpatterns = [
    url(r'^$', showHome, name='home'),
    url(r'^login$', login_view, name='login_view'),
    url(r'^admin/', admin.site.urls),
    url(r'^persons/', include('persons.urls',namespace='persons')),

    url('^', include('django.contrib.auth.urls')),
    url('^accounts/', include('accounts.urls',namespace='accounts')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)