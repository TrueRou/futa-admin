from enum import IntEnum, auto
from typing import List, Optional, Tuple

from sqlmodel import Field, SQLModel

from pyfuta.app.models.report.field import ReportFieldPublic
from pyfuta.app.models.report.fragment import ReportFragmentPublic
from pyfuta.app.models.report.mixin import ReportMixinPublic


class ReportType(IntEnum):
    FORM = auto()
    LINE_CHART = auto()
    BAR_CHART = auto()


class Report(SQLModel, table=True):
    __tablename__ = "def_reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    label: str
    sql: str
    type: ReportType
    linked_table: str = Field(default="")
    appendable: bool = Field(default=False)


class ReportCreate(SQLModel):
    label: str
    type: ReportType
    linked_table: Optional[str]
    appendable: Optional[bool]


class ReportUpdate(SQLModel):
    label: Optional[str]
    sql: Optional[str]
    type: Optional[ReportType]
    linked_table: Optional[str]
    appendable: Optional[bool]


class ReportPublic(SQLModel):
    id: int
    label: str
    type: ReportType
    linked_table: str
    appendable: bool


class ReportPublicFull(ReportPublic):
    fields: List[ReportFieldPublic]
    fragments: List[ReportFragmentPublic]
    mixins: List[ReportMixinPublic]
    data: List[Tuple]  # this will be the data returned from the table query


class ReportPublicAdmin(ReportPublic):
    sql: str


class ReportPublicFullAdmin(ReportPublicFull):
    sql: str
