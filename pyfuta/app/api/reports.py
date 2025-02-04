import json
from typing import Any, Dict, List, Union
from fastapi import APIRouter, Depends, HTTPException, Request
from pyfuta.app import database
from pyfuta.app.database import require_session
from pyfuta.app.models.report.field import ReportFieldCreate, ReportFieldUpdate
from pyfuta.app.models.report.fragment import ReportFragmentCreate, ReportFragmentPublic, ReportFragmentUpdate
from pyfuta.app.models.report.mixin import ReportMixinCreate
from pyfuta.app.models.report.report import ReportPublicAdmin
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


def require_report(report_id: int, session: Session = Depends(require_session)) -> Report:
    report = session.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


def require_field(field_id: int, session: Session = Depends(require_session)) -> ReportField:
    field = session.get(ReportField, field_id)
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return field


def require_fields(report: Report = Depends(require_report), session: Session = Depends(require_session)) -> List[ReportField]:
    fields = session.exec(select(ReportField).where(ReportField.report_id == report.id)).all()
    if len(fields) == 0:
        raise HTTPException(status_code=404, detail="Report has no fields")
    return fields


# region: Report Router
report_router = APIRouter(prefix="/reports", tags=["Reports"])


@report_router.post("", response_model=ReportPublic)
async def create_report(report: ReportCreate, session: Session = Depends(require_session)):
    new_report = Report(**report.model_dump(), sql="SELECT 1")
    database.add_model(session, new_report)
    return new_report


@report_router.get("", response_model=List[Union[ReportPublic]])
async def get_reports(session: Session = Depends(require_session)):
    reports = session.exec(select(Report))
    return reports


@report_router.get("/{report_id}", response_model=ReportPublicAdmin)
async def get_report(report: Report = Depends(require_report)):
    return report


@report_router.post("/{report_id}", response_model=Union[ReportPublicFull, ReportPublicFullAdmin])
async def query_report(
    request: Request,
    fragments: Dict[str, Any] = {},
    report: Report = Depends(require_report),
    fields: List[ReportField] = Depends(require_fields),
    session: Session = Depends(require_session),
):
    with_admin = request.headers.get("X-Admin", "0") == "1"
    fragments = {k: v for k, v in fragments.items() if v is not None}
    data = await dispatcher.dispatch_statement(report.sql, fragments, session, report.id)
    frags = session.exec(select(ReportFragment).where(ReportFragment.report_id == report.id))
    mixins = session.exec(select(ReportMixin).where(ReportMixin.report_id == report.id))
    report_full = ReportPublicFull(**report.model_dump(), fields=fields, data=data, fragments=frags, mixins=mixins)
    return ReportPublicFullAdmin(**report_full.model_dump(), sql=report.sql) if with_admin else report_full


@report_router.patch("/{report_id}", response_model=ReportPublic)
async def patch_report(updates: ReportUpdate, report: Report = Depends(require_report), session: Session = Depends(require_session)):
    database.partial_update_model(session, report, updates.model_dump())
    return report


@report_router.delete("/{report_id}")
async def delete_report(report: Report = Depends(require_report), session: Session = Depends(require_session)):
    database.delete_model(session, report)


@report_router.patch("/{report_id}/rows")
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
    field = require_field(field_id, session)
    nav_field = require_field(nav_field_id, session)
    if not field.linked_field or not nav_field.linked_field:
        raise HTTPException(status_code=404, detail="Field or nav field is not bound to a table field")
    value = field.type.parse(value)
    nav_value = nav_field.type.parse(nav_value)
    await dispatcher.dispatch_updating(report.linked_table, field.linked_field, nav_field.linked_field, value, nav_value)


@report_router.post("/{report_id}/rows")
async def insert_row_to_report(data: Dict[str, str], report: Report = Depends(require_report), session: Session = Depends(require_session)):
    if report.linked_table is None:
        raise HTTPException(status_code=404, detail="Report is not bound to a table")
    for key in data.keys():
        field = session.exec(select(ReportField).where(ReportField.report_id == report.id, ReportField.linked_field == key)).first()
        if field is None:
            raise HTTPException(status_code=404, detail=f"Field not found: {key}")
        data[key] = field.type.parse(data[key])
    await dispatcher.dispatch_inserting(report.linked_table, data)


@report_router.delete("/{report_id}/rows")
async def delete_row_from_report(primary_key_value: str, report: Report = Depends(require_report), session: Session = Depends(require_session)):
    if report.linked_table is None:
        raise HTTPException(status_code=404, detail="Report is not bound to a table")
    pk_field = session.exec(select(ReportField).order_by(ReportField.order).where(ReportField.report_id == report.id)).first()
    if pk_field is None:
        raise HTTPException(status_code=404, detail="Primary key not found for report")
    pk_value = pk_field.type.parse(primary_key_value)
    await dispatcher.dispatch_deleting(report.linked_table, pk_field.linked_field, pk_value)


# endregion: Report Router

# region: Field Router
field_router = APIRouter(prefix="/fields", tags=["Fields"])


@field_router.get("", response_model=List[ReportField])
async def get_fields(report_id: int, session: Session = Depends(require_session)):
    fields = session.exec(select(ReportField).where(ReportField.report_id == report_id)).all()
    return fields


@field_router.post("", response_model=ReportField, tags=["Fields"])
async def create_field(field: ReportFieldCreate, report: Report = Depends(require_report), session: Session = Depends(require_session)):
    if session.exec(select(ReportField).where(ReportField.report_id == report.id, ReportField.order == field.order)).first():
        raise HTTPException(status_code=400, detail="Order index already exists")
    field = ReportField(**field.model_dump(), report_id=report.id)
    database.add_model(session, field)
    return field


@field_router.patch("/{field_id}", response_model=ReportField)
async def patch_field(updates: ReportFieldUpdate, field: ReportField = Depends(require_field), session: Session = Depends(require_session)):
    if field.order != updates.order:
        # this is a reorder patch, we only update the order, no need to check other changes
        if target := session.exec(select(ReportField).where(ReportField.report_id == field.report_id, ReportField.order == updates.order)).first():
            target.order = field.order  # swap orders
        field.order = updates.order
        session.commit()
        return field  # return the updated field, skip the rest
    database.partial_update_model(session, field, updates.model_dump())
    return field


@field_router.delete("/{field_id}")
async def delete_field(field: ReportField = Depends(require_field), session: Session = Depends(require_session)):
    database.delete_model(session, field)


# endregion: Field Router

# region: Fragment Router
fragment_router = APIRouter(prefix="/fragments", tags=["Fragments"])


@fragment_router.get("", response_model=List[ReportFragment])
async def get_fragments(report_id: int, session: Session = Depends(require_session)):
    fragments = session.exec(select(ReportFragment).where(ReportFragment.report_id == report_id)).all()
    return fragments


@fragment_router.post("", response_model=ReportFragment)
async def create_fragment(fragment: ReportFragmentCreate, report: Report = Depends(require_report), session: Session = Depends(require_session)):
    try:
        if fragment.extends:
            json.loads(fragment.extends)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for extends")
    fragment = ReportFragment(**fragment.model_dump(), report_id=report.id)
    database.add_model(session, fragment)
    return fragment


@fragment_router.patch("/{fragment_id}", response_model=ReportFragment)
async def patch_fragment(fragment_id: int, updates: ReportFragmentUpdate, session: Session = Depends(require_session)):
    try:
        if updates.extends:
            json.loads(updates.extends)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for extends")
    fragment = session.get(ReportFragment, fragment_id)
    database.partial_update_model(session, fragment, updates.model_dump())
    return fragment


@fragment_router.delete("/{fragment_id}")
async def delete_fragment(fragment_id: int, session: Session = Depends(require_session)):
    fragment = session.get(ReportFragment, fragment_id)
    database.delete_model(session, fragment)


# endregion: Fragment Router

# region: Mixin Router
mixin_router = APIRouter(prefix="/mixins", tags=["Mixins"])


@mixin_router.get("", response_model=List[ReportMixin])
async def get_mixins(report_id: int, session: Session = Depends(require_session)):
    mixins = session.exec(select(ReportMixin).where(ReportMixin.report_id == report_id)).all()
    return mixins


@mixin_router.post("", response_model=ReportMixin)
async def create_mixin(mixin: ReportMixinCreate, report: Report = Depends(require_report), session: Session = Depends(require_session)):
    try:
        if mixin.values:
            json.loads(mixin.values)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for extends")
    mixin = ReportMixin(**mixin.model_dump(), report_id=report.id)
    database.add_model(session, mixin)
    return mixin


@mixin_router.patch("/{mixin_id}", response_model=ReportMixin)
async def patch_mixin(mixin_id: int, updates: ReportMixinCreate, session: Session = Depends(require_session)):
    try:
        if updates.values:
            json.loads(updates.values)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for values")
    mixin = session.get(ReportMixin, mixin_id)
    database.partial_update_model(session, mixin, updates.model_dump())
    return mixin


@mixin_router.delete("/{mixin_id}")
async def delete_mixin(mixin_id: int, session: Session = Depends(require_session)):
    mixin = session.get(ReportMixin, mixin_id)
    database.delete_model(session, mixin)


# endregion: Mixin Router

router = APIRouter()
[router.include_router(r) for r in [report_router, field_router, fragment_router, mixin_router]]
