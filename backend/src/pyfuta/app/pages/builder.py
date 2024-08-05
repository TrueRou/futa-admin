from pyfuta.app import database
from pyfuta.app.pages.models import Page, PageReport
from pyfuta.app.reports.builder import ReportBuilder


class PageBuilder:
    def __init__(self, path: str, title: str, description: str = None):
        self.page = Page(path=path, title=title, description=description)
        metadata.append(self)

    def reports(self, *reports: ReportBuilder):
        self.report_builders = reports
        self.page_reports: list[PageReport] = []
        return self


class Metadata(list[PageBuilder]):
    async def create_all(self):
        import pyfuta.app.defs.pages  # noqa

        async with database.async_session_ctx() as session:
            for page_builder in self:
                session.add(page_builder.page)
                await session.commit()  # This is necessary to get the id
                await session.refresh(page_builder.page)
                for report_builder in page_builder.report_builders:
                    page_builder.page_reports.append(PageReport(page_path=page_builder.page.path, report_id=report_builder.report_id))
                session.add_all(page_builder.page_reports)
            await session.commit()  # Apply the changes to all the transactions.


metadata: Metadata = Metadata()
