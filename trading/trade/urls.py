
from django.urls import path
from .views import TradeApiView

urlpatterns = [
    path('trade/', TradeApiView.as_view()),
]