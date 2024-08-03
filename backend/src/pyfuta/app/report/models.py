from enum import IntEnum, auto
from typing import Any
from sqlmodel import Field, SQLModel


class ReportFieldType(IntEnum):
    TEXT = auto()
    NUMBER = auto()

    def parse(self, value: Any) -> Any:
        if self == ReportFieldType.NUMBER:
            return int(value)
        return value


class Report(SQLModel, table=True):
    __tablename__ = "def_reports"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    sql: str
    update_table: str | None = Field(default=None)


class ReportField(SQLModel, table=True):
    __tablename__ = "def_report_fields"

    report_id: int = Field(foreign_key="def_reports.id", primary_key=True)
    field_pos: int = Field(primary_key=True)
    name: str
    type: ReportFieldType


# for navigating to certain field in certain table in order to update it
class ReportNavigation(SQLModel):
    __tablename__ = "def_report_navigation"

    report_id: int = Field(foreign_key="def_reports.id", primary_key=True)
    field_pos: int = Field(primary_key=True)
    table_name: str
    field_name: str
    # this is dense, report has its unique nav field, rather than the field itself
    # we keep its dense, so that we can support batch update in the future
    nav_field_name: str
    nav_field_type: ReportFieldType


class ReportFieldPublic(SQLModel):
    name: str
    type: ReportFieldType
    editable: bool


class ReportPublic(SQLModel):
    id: int
    name: str
    fields: list[ReportFieldPublic]
    data: list[tuple]  # this will be the data returned from the table query
