from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pyfuta.app.database import require_session
from pyfuta.app.report import dispatcher
from pyfuta.app.report.models import Report, Report, ReportField, ReportPublic, ReportNavigation
from sqlmodel import Session, select


router = APIRouter(prefix="/reports", tags=["reports"])


def require_report(report_id: int, session: Session = Depends(require_session)) -> Report:
    report = session.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


def require_field(field_pos: int, report: Report = Depends(require_report), session: Session = Depends(require_session)) -> Report:
    field = session.get(ReportField, (report.id, field_pos))
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return field


def require_fields(report: Report = Depends(require_report), session: Session = Depends(require_session)) -> list[ReportField]:
    fields = session.exec(select(ReportField).where(ReportField.report_id == report.id)).all()
    if len(fields) == 0:
        raise HTTPException(status_code=404, detail="Report has no fields")


@router.get("/{report_id}", response_model=ReportPublic)
async def get_reports(filter: dict[str, Any], report: Report = Depends(require_report), fields: list[ReportField] = Depends(require_fields)):
    data = await dispatcher.dispatch_statement(report.sql, filter)
    return ReportPublic(**report.model_dump(), fields=fields, data=data)


@router.patch("/{report_id}")
async def update_report(
    value: str,
    nav_value: str,
    report: Report = Depends(require_report),
    field: ReportField = Depends(require_field),
    session: Session = Depends(require_session),
):
    value = field.type.parse(value)
    nav_value = field.type.parse(nav_value)
    editable = session.get(ReportNavigation, (report.id, field.field_pos))
    if editable is None:
        raise HTTPException(status_code=404, detail="Field not editable")
    await dispatcher.dispatch_updating(editable.table_name, editable.field_name, value)
