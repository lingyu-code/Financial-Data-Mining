from rest_framework import serializers
from financial_data_mining.models import FinancialPaper, StockDaily

class FinancialPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialPaper
        fields = '__all__'

class StockDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDaily
        fields = '__all__'
