from typing import Any, Dict, List, Union
from fastapi import APIRouter, Depends, HTTPException, Request
from pyfuta.app import database
from pyfuta.app.database import require_session
from pyfuta.app.utils import dispatcher
from pyfuta.app.models.report import (
    Report,
    ReportCreate,
    ReportField,
    ReportFragment,
    ReportMixin,
    ReportPublic,
    ReportUpdate,
    ReportPublicFull,
    ReportPublicFullAdmin,
)
from sqlmodel import Session, select


router = APIRouter(prefix="/report", tags=["Report"])


def require_report(report_id: int, session: Session = Depends(require_session)) -> Report:
    report = session.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


def require_field(field_id: int, report: Report = Depends(require_report), session: Session = Depends(require_session)) -> ReportField:
    field = session.get(ReportField, (report.id, field_id))
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return field


def require_fields(report: Report = Depends(require_report), session: Session = Depends(require_session)) -> List[ReportField]:
    fields = session.exec(select(ReportField).where(ReportField.report_id == report.id)).all()
    if len(fields) == 0:
        raise HTTPException(status_code=404, detail="Report has no fields")
    return fields


@router.post("", response_model=ReportPublic)
async def create_report(report: ReportCreate, session: Session = Depends(require_session)):
    new_report = Report(**report.model_dump())
    database.add_model(session, new_report)
    return new_report


@router.post("/{report_id}", response_model=Union[ReportPublicFull, ReportPublicFullAdmin])
async def get_report(
    request: Request,
    fragments: Dict[str, Any] = {},
    report: Report = Depends(require_report),
    fields: List[ReportField] = Depends(require_fields),
    session: Session = Depends(require_session),
):
    with_admin = request.headers.get("X-Admin", False)
    fragments = {k: v for k, v in fragments.items() if v is not None}
    data = await dispatcher.dispatch_statement(report.sql, fragments, session, report.id)
    frags = session.exec(select(ReportFragment).where(ReportFragment.report_id == report.id))
    mixins = session.exec(select(ReportMixin).where(ReportMixin.report_id == report.id))
    report_full = ReportPublicFull(**report.model_dump(), fields=fields, data=data, fragments=frags, mixins=mixins)
    return ReportPublicFullAdmin(**report_full.model_dump(), sql=report.sql) if with_admin else report_full


@router.patch("/{report_id}", response_model=ReportPublic)
async def patch_report(updates: ReportUpdate, report: Report = Depends(require_report), session: Session = Depends(require_session)):
    database.partial_update_model(session, report, updates.model_dump())
    return report


@router.patch("/{report_id}/row")
async def patch_row_in_report(
    field_id: int,
    nav_field_id: int,
    value: str,
    nav_value: str,
    report: Report = Depends(require_report),
    session: Session = Depends(require_session),
):
    if report.linked_table is None:
        raise HTTPException(status_code=404, detail="Report is not bound to a table")
    field = require_field(field_id, report, session)
    nav_field = require_field(nav_field_id, report, session)
    if field.linked_field is None or nav_field.linked_field is None:
        raise HTTPException(status_code=404, detail="Field is not bound to a table field")
    value = field.type.parse(value)
    nav_value = nav_field.type.parse(nav_value)
    await dispatcher.dispatch_updating(report.linked_table, field.linked_field, nav_field.linked_field, value, nav_value)


@router.post("/{report_id}/row")
async def insert_row_to_report(
    data: Dict[str, str],
    report: Report = Depends(require_report),
    session: Session = Depends(require_session),
):
    if report.linked_table is None:
        raise HTTPException(status_code=404, detail="Report is not bound to a table")
    for key in data.keys():
        field = session.exec(select(ReportField).where(ReportField.report_id == report.id, ReportField.linked_field == key)).first()
        if field is None:
            raise HTTPException(status_code=404, detail=f"Field not found: {key}")
        data[key] = field.type.parse(data[key])
    await dispatcher.dispatch_inserting(report.linked_table, data)


@router.delete("/{report_id}/row")
async def delete_row_from_report(
    primary_key_value: str,
    report: Report = Depends(require_report),
    session: Session = Depends(require_session),
):
    if report.linked_table is None:
        raise HTTPException(status_code=404, detail="Report is not bound to a table")
    pk_field = session.exec(select(ReportField).where(ReportField.report_id == report.id, ReportField.index == True)).first()
    if pk_field is None:
        raise HTTPException(status_code=404, detail="Primary key not found for report")
    pk_value = pk_field.type.parse(primary_key_value)
    await dispatcher.dispatch_deleting(report.linked_table, pk_field.linked_field, pk_value)
