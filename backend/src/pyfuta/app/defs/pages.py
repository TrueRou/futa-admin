from pyfuta.app.pages.builder import PageBuilder
from pyfuta.app.defs.reports import *

PageBuilder(path="products", title="商品销售", description="商品销售情况汇总信息").reports(*products)
PageBuilder(path="consumers", title="商品客户", description="商品客户情况汇总信息").reports(*customers)
