from fastapi import APIRouter, Depends, HTTPException
from pyfuta.app.database import require_session
from pyfuta.app.pages.models import Page, PagePublic, PageReport
from pyfuta.app.reports.models import Report, ReportSimple
from sqlmodel import Session, select


router = APIRouter(prefix="/pages", tags=["pages"])


def require_page(page_id: int, session: Session = Depends(require_session)) -> Page:
    page = session.get(Page, page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.get("/", response_model=list[PagePublic])
async def get_pages(session: Session = Depends(require_session)):
    pages = session.exec(select(Page))
    results = []
    for page in pages:
        reports = session.exec(select(Report).join(PageReport).where(PageReport.page_id == page.id))
        simple_reports = [ReportSimple.model_validate(report) for report in reports]
        results.append(PagePublic(**page.model_dump(), reports=simple_reports))
    return results
