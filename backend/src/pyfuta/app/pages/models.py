from pyfuta.app.reports.models import ReportSimple
from sqlmodel import Field, SQLModel


class Page(SQLModel, table=True):
    __tablename__ = "def_pages"

    path: str = Field(primary_key=True)
    title: str
    description: str


class PageReport(SQLModel, table=True):
    __tablename__ = "def_page_reports"

    id: int | None = Field(default=None, primary_key=True)  # this is necessary
    page_path: str = Field(foreign_key="def_pages.path")
    report_id: int = Field(foreign_key="def_reports.id")


class PagePublic(SQLModel):
    path: str
    title: str
    description: str | None
    reports: list[ReportSimple]
