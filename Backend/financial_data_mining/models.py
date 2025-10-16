from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

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
