from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pyfuta.app import database
from pyfuta.app.api.reports import require_report
from pyfuta.app.database import require_session
from pyfuta.app.models.page import Page, PageCreate, PagePublic, PageReport, PageUpdate
from pyfuta.app.models.report import Report, ReportSimple
from sqlmodel import Session, select


router = APIRouter(prefix="/page", tags=["Pages"])


def require_page(path: str, session: Session = Depends(require_session)) -> Page:
    page = session.get(Page, path)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.get("", response_model=List[PagePublic])
async def get_pages(session: Session = Depends(require_session)):
    pages = session.exec(select(Page))
    results = []
    for page in pages:
        reports = session.exec(select(Report).join(PageReport).where(PageReport.page_path == page.path))
        simple_reports = [ReportSimple.model_validate(report) for report in reports]
        results.append(PagePublic(**page.model_dump(), reports=simple_reports))
    return results


@router.post("/{path}", response_model=PagePublic)
async def create_page(path: str, page: PageCreate, session: Session = Depends(require_session)):
    new_page = Page(**page.model_dump(), path=path)
    database.add_model(session, new_page)
    return new_page


@router.get("/{path}", response_model=PagePublic)
async def get_page(page: Page = Depends(require_page)):
    return page


@router.patch("/{path}", response_model=PagePublic)
async def patch_page(updates: PageUpdate, page: Page = Depends(require_page), session: Session = Depends(require_session)):
    if updates.path and updates.path != page.path:
        if session.get(Page, updates.path):
            raise HTTPException(status_code=400, detail="Path already exists")
    database.partial_update_model(session, page, updates)
    return page


@router.delete("/{path}", response_model=PagePublic)
async def delete_page(page: Page = Depends(require_page), session: Session = Depends(require_session)):
    session.delete(page)
    session.commit()
    return {"message": "Page deleted successfully"}


@router.post("/{path}/report/{report_id}")
async def add_report_to_page(
    report: Report = Depends(require_report),
    page: Page = Depends(require_page),
    session: Session = Depends(require_session),
):
    page_report = PageReport(page_path=page.path, report_id=report.id)
    database.add_model(session, page_report)
    return {"message": "Report added to page successfully"}


@router.delete("/{path}/report/{report_id}")
async def remove_report_from_page(
    report: Report = Depends(require_report),
    page: Page = Depends(require_page),
    session: Session = Depends(require_session),
):
    page_report = session.exec(select(PageReport).where(PageReport.page_path == page.path, PageReport.report_id == report.id)).first()
    if not page_report:
        raise HTTPException(status_code=404, detail="Report not found on page")
    session.delete(page_report)
    session.commit()
    return {"message": "Report removed from page successfully"}
