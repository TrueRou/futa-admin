from enum import IntEnum, auto
from typing import Dict, Optional
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class ReportFragmentType(IntEnum):
    FILTER_SELECT = auto()
    FILTER_DATERANGE = auto()
    FILTER_DATEDAY = auto()
    FILTER_DATEMONTH = auto()


class ReportFragment(SQLModel, table=True):
    __tablename__ = "def_report_fragments"

    id: Optional[int] = Field(default=None, primary_key=True)
    trait: str
    label: str
    type: ReportFragmentType
    sql: str
    values: Dict = Field(sa_column=Column(JSON), default_factory=dict)

    report_id: int = Field(foreign_key="def_reports.id", index=True)


class ReportFragmentCreate(SQLModel):
    trait: str
    label: str
    type: ReportFragmentType
    sql: str
    values: Dict


class ReportFragmentUpdate(SQLModel):
    trait: Optional[str]
    label: Optional[str]
    type: Optional[ReportFragmentType]
    sql: Optional[str]
    values: Optional[Dict]


class ReportFragmentPublic(SQLModel):
    id: int
    trait: str
    label: str
    type: ReportFragmentType
    values: Dict


class ReportFragmentPublicAdmin(ReportFragmentPublic):
    sql: str
