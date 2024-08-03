from enum import IntEnum, auto
from typing import Any
from sqlmodel import Field, SQLModel

metadata = SQLModel.metadata


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
    table_name: str | None = Field(default=None)


class ReportField(SQLModel, table=True):
    __tablename__ = "def_report_fields"

    report_id: int = Field(foreign_key="def_reports.id", primary_key=True)
    field_pos: int = Field(primary_key=True)
    name: str
    type: ReportFieldType
    field_name: str | None = Field(default=None)


class ReportFieldPublic(SQLModel):
    name: str
    type: ReportFieldType


class ReportPublic(SQLModel):
    id: int
    name: str
    fields: list[ReportFieldPublic]
    data: list[tuple]  # this will be the data returned from the table query
