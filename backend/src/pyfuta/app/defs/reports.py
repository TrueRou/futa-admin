from pyfuta.app.reports.builder import ReportBuilder

sales = ReportBuilder(name="Sales", sql="SELECT * FROM sales", table_name="sales").fields("id", "name", "price")
products = ReportBuilder(name="Products", sql="SELECT * FROM products", table_name="products").fields("id", "name", "price")
customers = ReportBuilder(name="Customers", sql="SELECT * FROM customers", table_name="customers").fields("id", "name", "phone")
