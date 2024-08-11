from pyfuta.app.reports.builder import DateTime, FragmentBuilder, Number, ReportBuilder, Text
from pyfuta.app.reports.models import ReportType

products = [
    ReportBuilder(name="Products", sql="SELECT * FROM products", table_name="products").fields(
        Number("编号", "id", pk=True), Text("商品名称", "name"), Number("价格", "price")
    ),
    ReportBuilder(name="Prices", sql="SELECT name, price FROM products").chart(ReportType.LINE_CHART, "商品名称", "价格"),
]

customers = [
    ReportBuilder(name="Customers", sql="SELECT * FROM customers ${interval}", table_name="customers").fields(
        Number("编号", "id", pk=True), Text("名称", "name"), Number("电话", "phone"), DateTime("创建时间", "created_at")
    )
]

fragments = [FragmentBuilder(locator="interval", fragment="WHERE created_at > DATETIME('now', ${value})")]
