from datetime import datetime
from enum import IntEnum, auto
from typing import Optional, Union

from sqlmodel import Field, SQLModel

from pyfuta.app.utils.executor import safe_execute


class ReportFieldType(IntEnum):
    TEXT = auto()
    NUMBER = auto()
    DATETIME = auto()

    def parse(self, value: str) -> Union[str, float, datetime]:
        if self == ReportFieldType.NUMBER:
            return safe_execute(float, 0, value)
        if self == ReportFieldType.DATETIME:
            return safe_execute(lambda: datetime.strptime(value, "%Y-%m-%d %H:%M:%S"), "")
        return value


class ReportField(SQLModel, table=True):
    __tablename__ = "def_report_fields"

    id: Optional[int] = Field(default=None, primary_key=True)
    order: int
    label: str
    type: ReportFieldType
    linked_field: str = Field(default="")

    report_id: int = Field(foreign_key="def_reports.id", index=True)


class ReportFieldCreate(SQLModel):
    order: int
    label: str
    type: ReportFieldType
    linked_field: Optional[str]


class ReportFieldUpdate(SQLModel):
    order: Optional[int]
    label: Optional[str]
    type: Optional[ReportFieldType]
    linked_field: Optional[str]


class ReportFieldPublic(SQLModel):
    id: int
    order: int
    label: str
    type: ReportFieldType
    linked_field: str
