from pyfuta.app import database
from pyfuta.app.report.models import Report, ReportField, ReportFieldType
from sqlalchemy import delete


class Text:
    def __init__(self, name: str, field_name: str = None):
        self.name = name
        self.type = ReportFieldType.TEXT
        self.field_name = field_name


class Number:
    def __init__(self, name: str, field_name: str = None):
        self.name = name
        self.type = ReportFieldType.NUMBER
        self.field_name = field_name


class Report:
    def __init__(self, name: str, sql: str, table_name: str):
        self.object = Report(name=name, sql=sql, table_name=table_name)
        self.field_pos = 0
        self.report_fields = []
        metadata.append(self)

    def fields(self, *fields: list[str | Text | Number]):
        for field in fields:
            field = Text(name=field) if isinstance(field, str) else field
            self.report_fields.append(ReportField(field_pos=self.field_pos, name=field.name, type=field.type, field_name=field.field_name))
            self.field_pos += 1


class Metadata(list[Report]):
    async def create_all(self):
        import pyfuta.app.defs.reports  # noqa

        async with database.async_session_ctx() as session:
            # Builder is the only one that can alter the table, so we can safely recreate the tables.
            # This is a simple way to handle migrations, until we need to support dynamic creation.
            await session.execute(delete(ReportField))
            await session.execute(delete(Report))
            await session.commit()  # Save the changes to the database.
            for builder in self:
                session.add(builder.object)
                if isinstance(builder, Report):
                    await session.commit()  # This is necessary to get the id
                    await session.refresh(builder.object)
                    for field in builder.report_fields:
                        field.report_id = builder.object.id
                    session.add_all(builder.report_fields)
            await session.commit()  # Apply the changes to all the transactions.


metadata: Metadata = Metadata()
