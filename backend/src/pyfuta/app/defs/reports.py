from pyfuta.app.reports.builder import Number, ReportBuilder, Text

sales = ReportBuilder(name="Sales", sql="SELECT * FROM sales", table_name="sales").fields(
    Number("编号", "id", pk=True), Text("名称", "name"), Number("价格", "price")
)
products = ReportBuilder(name="Products", sql="SELECT * FROM products").fields("id", "name", "price")
customers = ReportBuilder(name="Customers", sql="SELECT * FROM customers").fields("id", "name", "phone")
