from fastapi import APIRouter

from pyfuta.app.api import imports, pages, reports

router = APIRouter()

router.include_router(pages.router)
router.include_router(reports.router)
router.include_router(imports.router)
