from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pyfuta.app import database
from pyfuta.app.api.reports import require_report
from pyfuta.app.database import require_session
from pyfuta.app.models.page import Page, PageCreate, PagePublic, PageReport, PageUpdate
from pyfuta.app.models.report import Report
from sqlmodel import Session, select

from pyfuta.app.models.report.report import ReportPublic


router = APIRouter(prefix="/pages", tags=["Pages"])


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
        simple_reports = [ReportPublic.model_validate(report) for report in reports]
        results.append(PagePublic(**page.model_dump(), reports=simple_reports))
    return results


@router.post("/{path}", response_model=PagePublic)
async def create_page(path: str, page: PageCreate, session: Session = Depends(require_session)):
    if session.get(Page, path):
        raise HTTPException(status_code=400, detail="Path already exists")
    if path == "":
        raise HTTPException(status_code=400, detail="Path cannot be empty string")
    new_page = Page(**page.model_dump(), path=path)
    database.add_model(session, new_page)
    return PagePublic(**new_page.model_dump(), reports=[])


@router.get("/{path}", response_model=PagePublic)
async def get_page(page: Page = Depends(require_page), session: Session = Depends(require_session)):
    reports = session.exec(select(Report).join(PageReport).where(PageReport.page_path == page.path))
    simple_reports = [ReportPublic.model_validate(report) for report in reports]
    return PagePublic(**page.model_dump(), reports=simple_reports)


@router.patch("/{path}", response_model=PagePublic)
async def patch_page(updates: PageUpdate, page: Page = Depends(require_page), session: Session = Depends(require_session)):
    if updates.path and updates.path != page.path:
        if session.get(Page, updates.path):
            raise HTTPException(status_code=400, detail="Path already exists")
    if updates.path == "":
        raise HTTPException(status_code=400, detail="Path cannot be empty string")
    database.partial_update_model(session, page, updates)
    return PagePublic(**page.model_dump(), reports=[])


@router.delete("/{path}")
async def delete_page(page: Page = Depends(require_page), session: Session = Depends(require_session)):
    page_reports = session.exec(select(PageReport).where(PageReport.page_path == page.path)).all()
    [session.delete(page_report) for page_report in page_reports]
    session.delete(page)
    session.commit()
    return {"message": "Page deleted successfully"}


@router.post("/{path}/reports/{report_id}")
async def add_report_to_page(
    report: Report = Depends(require_report),
    page: Page = Depends(require_page),
    session: Session = Depends(require_session),
):
    page_report = PageReport(page_path=page.path, report_id=report.id)
    database.add_model(session, page_report)
    return {"message": "Report added to page successfully"}


@router.delete("/{path}/reports/{report_id}")
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
