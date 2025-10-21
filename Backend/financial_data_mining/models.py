from django.db import models

class FinancialPaper(models.Model):
    title = models.CharField(max_length=200, verbose_name="论文标题")
    author = models.CharField(max_length=100, verbose_name="作者")
    abstract = models.TextField(blank=True, null=True, verbose_name="摘要")
    pdf_file = models.FileField(upload_to='financial_papers/', verbose_name="PDF文件")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="上传日期")
    keywords = models.CharField(max_length=200, blank=True, null=True, verbose_name="关键词")

    class Meta:
        verbose_name = "金融论文"
        verbose_name_plural = "金融论文"

    def __str__(self):
        return self.title

# rawdata.py
class StockDaily(models.Model):
    ts_code = models.CharField(max_length=20, db_index=True, verbose_name="股票代码")
    trade_date = models.DateField(verbose_name="交易日期")
    open = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="开盘价")
    high = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="最高价")
    low = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="最低价")
    close = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="收盘价")
    volume = models.BigIntegerField(verbose_name="成交量")

    class Meta:
        db_table = "stock_daily"
        unique_together = ("ts_code", "trade_date")  # 保证同一股票同一天只有一条数据
        indexes = [
            models.Index(fields=["ts_code", "trade_date"]),
        ]
        verbose_name = "股票日行情"
        verbose_name_plural = "股票日行情"

    def __str__(self):
        return f"{self.ts_code} - {self.trade_date}"
