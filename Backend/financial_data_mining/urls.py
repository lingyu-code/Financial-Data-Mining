from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from financial_data_mining.viewsets import StockDailyViewSet, FinancialPaperViewSet

router = DefaultRouter()
router.register(r'stocks', StockDailyViewSet, basename='stocks')
router.register(r'papers', FinancialPaperViewSet, basename='papers')

urlpatterns = [
    path('', include(router.urls)),
]
