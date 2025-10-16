from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from financial_data_mining.viewsets import StockDailyViewSet, BookViewSet

router = DefaultRouter()
router.register(r'stocks', StockDailyViewSet, basename='stocks')
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
]
