from pyfuta.app.report.builder import Report

Report(name="Sales", sql="SELECT * FROM sales", table_name="sales").fields("id", "name", "price")
Report(name="Products", sql="SELECT * FROM products", table_name="products").fields("id", "name", "price")
Report(name="Customers", sql="SELECT * FROM customers", table_name="customers").fields("id", "name", "phone")
