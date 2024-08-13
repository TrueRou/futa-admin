from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pyfuta.app.database import require_session
from pyfuta.app.reports import dispatcher
from pyfuta.app.reports.models import Report, ReportField, ReportFragment, ReportFragmentPublic, ReportPublic
from sqlmodel import Session, select


router = APIRouter(prefix="/reports", tags=["reports"])


def require_report(report_id: int, session: Session = Depends(require_session)) -> Report:
    report = session.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


def require_field(field_pos: int, report: Report = Depends(require_report), session: Session = Depends(require_session)) -> ReportField:
    field = session.get(ReportField, (report.id, field_pos))
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return field


def require_fields(report: Report = Depends(require_report), session: Session = Depends(require_session)) -> list[ReportField]:
    fields = session.exec(select(ReportField).where(ReportField.report_id == report.id)).all()
    if len(fields) == 0:
        raise HTTPException(status_code=404, detail="Report has no fields")
    return fields


@router.post("/{report_id}", response_model=ReportPublic)
async def get_reports(
    fragments: dict[str, Any] = {},
    report: Report = Depends(require_report),
    fields: list[ReportField] = Depends(require_fields),
    session: Session = Depends(require_session),
):
    fragments = {k: v for k, v in fragments.items() if v is not None}
    data = await dispatcher.dispatch_statement(report.sql, fragments, session, report.id)
    frags = [
        ReportFragmentPublic(**frag.model_dump(exclude=["values"]), values=frag.values.split(",") if frag.values is not None else None)
        for frag in session.exec(select(ReportFragment).where(ReportFragment.report_id == report.id))
    ]
    return ReportPublic(**report.model_dump(), fields=fields, data=data, fragments=frags)


@router.patch("/{report_id}")
async def patch_report(
    field_pos: int,
    nav_field_pos: int,
    value: str,
    nav_value: str,
    report: Report = Depends(require_report),
    session: Session = Depends(require_session),
):
    if report.table_name is None:
        raise HTTPException(status_code=404, detail="Report is not bound to a table")
    field = require_field(field_pos, report, session)
    nav_field = require_field(nav_field_pos, report, session)
    if field.field_name is None or nav_field.field_name is None:
        raise HTTPException(status_code=404, detail="Field is not bound to a table field")
    value = field.type.parse(value)
    nav_value = nav_field.type.parse(nav_value)
    await dispatcher.dispatch_updating(report.table_name, field.field_name, nav_field.field_name, value, nav_value)
