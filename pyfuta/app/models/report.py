from datetime import datetime
from enum import IntEnum, auto
from typing import Any, List, Optional
from sqlalchemy import JSON, Column, DateTime, Float, String
from sqlmodel import Field, SQLModel

metadata = SQLModel.metadata


class ReportType(IntEnum):
    # CHART: from 11 to 20 (this is quite arbitrary, maybe we can change it later)
    FORM = 1
    EXCEL_TABLE = 2
    LINE_CHART = 11
    BAR_CHART = 12


class ReportFragmentType(IntEnum):
    # FILTER: from 1 to 10 (this is quite arbitrary, maybe we can change it later)
    FILTER_SELECT = 1
    FILTER_DATERANGE = 2
    FILTER_DATEDAY = 3
    FILTER_DATEMONTH = 4


class ReportFieldType(IntEnum):
    TEXT = auto()
    NUMBER = auto()
    DATETIME = auto()

    def parse(self, value: str) -> Any:
        if self == ReportFieldType.NUMBER:
            try:
                return float(value)
            except ValueError:
                return 0
        if self == ReportFieldType.DATETIME:
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None
        return value

    def as_sqla(self) -> Any:
        if self == ReportFieldType.NUMBER:
            return Float
        if self == ReportFieldType.TEXT:
            return String
        if self == ReportFieldType.DATETIME:
            return DateTime


class Report(SQLModel, table=True):
    __tablename__ = "def_reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sql: str
    type: ReportType = Field(default=ReportType.FORM)
    table_name: Optional[str] = Field(default=None)
    is_editable: bool = Field(default=False)
    updateable_fields_only: bool = Field(default=False)


class ReportField(SQLModel, table=True):
    __tablename__ = "def_report_fields"

    report_id: int = Field(foreign_key="def_reports.id", primary_key=True)
    field_id: int = Field(primary_key=True)
    name: str
    type: ReportFieldType
    field_name: Optional[str] = Field(default=None)
    is_primary_key: bool = Field(default=False)
    is_fixed: bool = Field(default=False)
    width: Optional[int] = Field(default=None)

    def to_column(self):
        return


class ReportFragment(SQLModel, table=True):
    __tablename__ = "def_report_fragments"

    report_id: int = Field(foreign_key="def_reports.id", primary_key=True)
    trait: str = Field(primary_key=True)
    sql: str
    name: str
    type: ReportFragmentType = Field(default=ReportFragmentType.FILTER_SELECT)
    labels: Optional[str] = Field(default=None)  # only for FILTER_SELECT, (split by ,)
    values: Optional[str] = Field(default=None)  # only for FILTER_SELECT, (split by ,)


class ReportMixin(SQLModel, table=True):
    __tablename__ = "def_report_mixins"

    report_id: int = Field(foreign_key="def_reports.id", primary_key=True)
    ref_variable: str = Field(default="option", primary_key=True)
    values: dict = Field(sa_column=Column(JSON), default_factory=dict)
    sideload_sql: Optional[str] = Field(default=None)


class ReportFieldPublic(SQLModel):
    name: str
    field_id: int
    type: ReportFieldType
    field_name: Optional[str]
    is_fixed: bool
    width: Optional[int]


class ReportFragmentPublic(SQLModel):
    trait: str
    name: str
    type: ReportFragmentType
    labels: List[str]
    values: List[str]


class ReportMixinPublic(SQLModel):
    ref_variable: str
    values: dict


class ReportSimple(SQLModel):
    id: int
    name: str
    type: ReportType = Field(default=ReportType.FORM)


class ReportPublic(SQLModel):
    id: int
    name: str
    type: ReportType = Field(default=ReportType.FORM)
    is_editable: bool
    updateable_fields_only: bool
    fields: List[ReportFieldPublic]
    fragments: List[ReportFragmentPublic]
    mixins: List[ReportMixinPublic]
    data: List[tuple]  # this will be the data returned from the table query
