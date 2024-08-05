from pyfuta.app.reports.builder import Number, ReportBuilder, Text

sales = ReportBuilder(name="Sales", sql="SELECT * FROM sales", table_name="sales").fields(
    Number("编号", "id", pk=True), Text("名称", "name"), Number("价格", "price"), Number("折扣", "discount")
)
products = ReportBuilder(name="Products", sql="SELECT * FROM products", table_name="products").fields(
    Number("编号", "id", pk=True), Text("名称", "name"), Number("价格", "price")
)
customers = ReportBuilder(name="Customers", sql="SELECT * FROM customers", table_name="customers").fields(
    Number("编号", "id", pk=True), Text("名称", "name"), Number("电话", "phone")
)
