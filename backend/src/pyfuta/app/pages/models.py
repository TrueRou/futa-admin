from pyfuta.app.reports.models import ReportSimple
from sqlmodel import Field, SQLModel


class Page(SQLModel, table=True):
    __tablename__ = "def_pages"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str


class PageReport(SQLModel, table=True):
    __tablename__ = "def_page_reports"

    id: int | None = Field(default=None, primary_key=True)  # this is necessary
    page_id: int = Field(foreign_key="def_pages.id")
    report_id: int = Field(foreign_key="def_reports.id")


class PagePublic(SQLModel):
    title: str
    description: str | None
    reports: list[ReportSimple]
