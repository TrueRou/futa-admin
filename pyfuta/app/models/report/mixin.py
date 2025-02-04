from typing import Optional
from sqlmodel import Field, SQLModel


class ReportMixin(SQLModel, table=True):
    __tablename__ = "def_report_mixins"

    id: Optional[int] = Field(default=None, primary_key=True)
    ref_variable: str = Field(default="option")
    values: str = Field(default="")

    report_id: int = Field(foreign_key="def_reports.id", index=True)


class ReportMixinCreate(SQLModel):
    ref_variable: str
    values: str


class ReportMixinUpdate(SQLModel):
    ref_variable: Optional[str]
    values: Optional[str]


class ReportMixinPublic(SQLModel):
    id: int
    ref_variable: str
    values: str
