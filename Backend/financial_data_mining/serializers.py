from rest_framework import serializers
from financial_data_mining.models import Book, StockDaily

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class StockDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDaily
        fields = '__all__'
