from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('watchlist.api.urls')),

    # for rest framework default temp login view
    path('api-auth/', include('rest_framework.urls')),
]
