from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from financial_data_mining.models import Book, StockDaily
from financial_data_mining.serializers import BookSerializer, StockDailySerializer
import csv, io
from datetime import datetime
from decimal import Decimal


class BookViewSet(viewsets.ModelViewSet):
    """图书管理"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class StockDailyViewSet(viewsets.ModelViewSet):
    """
    股票日行情视图集
    提供标准 CRUD 接口 + CSV 上传接口
    """
    queryset = StockDaily.objects.all().order_by('-trade_date')
    serializer_class = StockDailySerializer

    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        """
        上传 CSV 文件并保存到数据库
        需包含列名: ts_code, trade_date, open, high, low, close, volume
        """
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "没有文件"}, status=status.HTTP_400_BAD_REQUEST)
        print("📂 收到上传文件:", file)
        print("📏 文件大小:", file.size, "bytes")
        print("📁 文件名:", file.name)
        try:
            decoded_file = file.read().decode('utf-8-sig')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            required_fields = ["ts_code", "trade_date", "open", "high", "low", "close", "volume"]
            for field in required_fields:
                if field not in reader.fieldnames:
                    return Response({"error": f"CSV 文件缺少必要字段：{field}"}, status=status.HTTP_400_BAD_REQUEST)

            created_count = 0
            skipped_count = 0
            errors = []

            for row in reader:
                try:
                    ts_code = row["ts_code"].strip()
                    trade_date = datetime.strptime(row["trade_date"].strip(), "%Y%m%d").date()
                    open_price = Decimal(row["open"])
                    high_price = Decimal(row["high"])
                    low_price = Decimal(row["low"])
                    close_price = Decimal(row["close"])
                    volume = int(float(row["volume"]))  # 有些 CSV volume 是小数

                    obj, created = StockDaily.objects.update_or_create(
                        ts_code=ts_code,
                        trade_date=trade_date,
                        defaults={
                            "open": open_price,
                            "high": high_price,
                            "low": low_price,
                            "close": close_price,
                            "volume": volume,
                        }
                    )

                    if created:
                        created_count += 1
                    else:
                        skipped_count += 1

                except Exception as e:
                    errors.append(str(e))

            return Response({
                "message": "导入完成",
                "created": created_count,
                "updated": skipped_count,
                "errors": errors[:5],  # 只显示前5个错误
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
