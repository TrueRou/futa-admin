from pyfuta.app.pages.builder import PageBuilder
from pyfuta.app.defs.reports import sales, products, customers

PageBuilder(path="marketing", title="Marketing", description="Marketing contains sales and relevant stuff").reports(sales, products, customers)
