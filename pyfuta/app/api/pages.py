from fastapi import APIRouter, Depends
from pyfuta.app.database import require_session
from pyfuta.app.models.page import Page, PagePublic, PageReport
from pyfuta.app.models.report import Report, ReportSimple
from sqlmodel import Session, select


router = APIRouter(prefix="/page", tags=["Pages"])


@router.get("/", response_model=list[PagePublic])
async def get_pages(session: Session = Depends(require_session)):
    pages = session.exec(select(Page))
    results = []
    for page in pages:
        reports = session.exec(select(Report).join(PageReport).where(PageReport.page_path == page.path))
        simple_reports = [ReportSimple.model_validate(report) for report in reports]
        results.append(PagePublic(**page.model_dump(), reports=simple_reports))
    return results
