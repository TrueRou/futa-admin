from pyfuta.app.pages.builder import PageBuilder
from pyfuta.app.defs.reports import sales, products, customers

PageBuilder(title="Marketing", description="Marketing contains sales and relevant stuff").reports(sales, products, customers)
