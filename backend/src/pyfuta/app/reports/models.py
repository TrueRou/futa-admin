from enum import IntEnum, auto
from typing import Any
from sqlalchemy import DateTime, Float, String
from sqlmodel import Field, SQLModel

metadata = SQLModel.metadata


class ReportType(IntEnum):
    FORM = auto()
    EXCEL_TABLE = auto()
    LINE_CHART = auto()
    BAR_CHART = auto()


class ReportFieldType(IntEnum):
    TEXT = auto()
    NUMBER = auto()
    DATETIME = auto()

    def parse(self, value: Any) -> Any:
        if self == ReportFieldType.NUMBER:
            return float(value)  # we consider all numbers as floats
        if self == ReportFieldType.DATETIME:
            raise NotImplementedError("Datetime parsing is not implemented")
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

    id: int | None = Field(default=None, primary_key=True)
    name: str
    sql: str
    type: ReportType = Field(default=ReportType.FORM)
    table_name: str | None = Field(default=None)


class ReportField(SQLModel, table=True):
    __tablename__ = "def_report_fields"

    report_id: int = Field(foreign_key="def_reports.id", primary_key=True)
    field_pos: int = Field(primary_key=True)
    name: str
    type: ReportFieldType
    field_name: str | None = Field(default=None)
    is_primary_key: bool = Field(default=False)

    def to_column(self):
        return


class ReportFieldPublic(SQLModel):
    name: str
    type: ReportFieldType
    field_name: str | None


class ReportSimple(SQLModel):
    id: int
    name: str
    type: ReportType = Field(default=ReportType.FORM)


class ReportPublic(SQLModel):
    id: int
    name: str
    type: ReportType = Field(default=ReportType.FORM)
    fields: list[ReportFieldPublic]
    data: list[tuple]  # this will be the data returned from the table query
