from typing import Optional
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class ReportMixin(SQLModel, table=True):
    __tablename__ = "def_report_mixins"

    id: Optional[int] = Field(default=None, primary_key=True)
    ref_variable: str = Field(default="option", primary_key=True)
    values: dict = Field(sa_column=Column(JSON), default_factory=dict)

    report_id: int = Field(foreign_key="def_reports.id", index=True)


class ReportMixinCreate(SQLModel):
    ref_variable: str
    values: dict


class ReportMixinUpdate(SQLModel):
    ref_variable: Optional[str]
    values: Optional[dict]


class ReportMixinPublic(SQLModel):
    id: int
    ref_variable: str
    values: dict
