from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from financial_data_mining.models import FinancialPaper, StockDaily
from financial_data_mining.serializers import FinancialPaperSerializer, StockDailySerializer
import csv, io
from datetime import datetime
from decimal import Decimal


class FinancialPaperViewSet(viewsets.ModelViewSet):
    """金融论文管理"""
    queryset = FinancialPaper.objects.all().order_by('-upload_date')
    serializer_class = FinancialPaperSerializer

    @action(detail=False, methods=['post'])
    def upload_pdf(self, request):
        """
        上传PDF文件并保存论文信息
        """
        try:
            title = request.data.get('title', '')
            author = request.data.get('author', '')
            abstract = request.data.get('abstract', '')
            keywords = request.data.get('keywords', '')
            pdf_file = request.FILES.get('pdf_file')

            if not pdf_file:
                return Response({"error": "请选择PDF文件"}, status=status.HTTP_400_BAD_REQUEST)

            if not title:
                return Response({"error": "请输入论文标题"}, status=status.HTTP_400_BAD_REQUEST)

            # 检查文件类型
            if not pdf_file.name.lower().endswith('.pdf'):
                return Response({"error": "请上传PDF格式的文件"}, status=status.HTTP_400_BAD_REQUEST)

            # 创建论文记录
            paper = FinancialPaper.objects.create(
                title=title,
                author=author,
                abstract=abstract,
                keywords=keywords,
                pdf_file=pdf_file
            )

            serializer = FinancialPaperSerializer(paper)
            return Response({
                "message": "论文上传成功",
                "paper": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def analyze(self, request, pk=None):
        """
        分析论文内容
        """
        try:
            paper = self.get_object()
            
            # 这里可以添加实际的论文分析逻辑
            # 目前返回模拟的分析结果
            analysis_result = {
                "paper_id": paper.id,
                "title": paper.title,
                "author": paper.author,
                "word_count": len(paper.abstract or "") + len(paper.title or "") + len(paper.keywords or ""),
                "keyword_analysis": {
                    "total_keywords": len(paper.keywords.split(',')) if paper.keywords else 0,
                    "keywords": paper.keywords.split(',') if paper.keywords else []
                },
                "abstract_analysis": {
                    "length": len(paper.abstract or ""),
                    "sentences": len((paper.abstract or "").split('。')) if paper.abstract else 0
                },
                "themes": ["金融", "数据分析", "经济"] if "金融" in (paper.title or "") else ["其他"],
                "recommendations": [
                    "建议进一步研究相关数据模型",
                    "可以考虑结合机器学习方法",
                    "建议扩展实证分析部分"
                ]
            }
            
            return Response({
                "paper": FinancialPaperSerializer(paper).data,
                "analysis": analysis_result
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
