
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from news_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_app.urls')),
    path('account/', include('accounts.urls')),
    path('accounts/login/', RedirectView.as_view(pattern_name='login', query_string=True)),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

