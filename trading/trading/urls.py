from django.contrib import admin
from django.urls import path, include
from trade import urls as trade_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(trade_urls))
]