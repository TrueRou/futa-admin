from typing import List, Optional
from pyfuta.app.models.report import ReportPublic
from sqlmodel import Field, SQLModel


class Page(SQLModel, table=True):
    __tablename__ = "def_pages"

    path: str = Field(primary_key=True)
    name: str
    description: str = Field(default="")


class PageReport(SQLModel, table=True):
    __tablename__ = "def_page_reports"

    id: Optional[int] = Field(default=None, primary_key=True)  # this is necessary
    page_path: str = Field(foreign_key="def_pages.path")
    report_id: int = Field(foreign_key="def_reports.id")


class PageCreate(SQLModel):
    name: str
    description: str


class PageUpdate(SQLModel):
    path: Optional[str]
    name: Optional[str]
    description: Optional[str]


class PagePublic(SQLModel):
    path: str
    name: str
    description: Optional[str]
    reports: List[ReportPublic]
