from pyfuta.app import database
from pyfuta.app.reports.models import Report, ReportField, ReportFieldType, ReportType
from sqlalchemy import Column, Table
from sqlmodel import SQLModel


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


class ReportBuilder:
    def __init__(self, name: str, sql: str, table_name: str = None):
        self.report = Report(name=name, sql=sql, table_name=table_name)
        self.field_pos: int = 0
        self.report_id: int = -1
        self.report_fields: list[ReportField] = []
        metadata.append(self)

    def fields(self, *fields: str | Text | Number):
        for field in fields:
            field = Text(name=field) if isinstance(field, str) else field
            self.report_fields.append(ReportField(field_pos=self.field_pos, name=field.name, type=field.type, field_name=field.field_name))
            self.field_pos += 1
        return self

    def chart(self, chart_type: ReportType, x_field: str, y_field: str):
        self.report.type = chart_type
        self.fields(x_field, Number(y_field))
        return self

    def _create_table(self):
        table = Table(
            self.report.table_name,
            SQLModel.metadata,
            [Column(field.field_name, field.type.as_sqla(), primary_key=field.is_primary_key) for field in self.report_fields],
        )
        SQLModel.metadata.create_all(database.engine, tables=[table])


class Metadata(list[ReportBuilder]):
    async def create_all(self):
        import pyfuta.app.defs.reports  # noqa

        async with database.async_session_ctx() as session:
            for builder in self:
                session.add(builder.report)
                await session.commit()  # This is necessary to get the id
                await session.refresh(builder.report)
                builder.report_id = builder.report.id
                for field in builder.report_fields:
                    field.report_id = builder.report.id
                session.add_all(builder.report_fields)
            await session.commit()  # Apply the changes to all the transactions.

        SQLModel.metadata.create_all(
            database.engine,
            [
                Table(
                    builder.report.table_name,
                    SQLModel.metadata,
                    [
                        Column(field.field_name, field.type.as_sqla(), primary_key=field.is_primary_key)
                        for field in builder.report_fields
                        if field.field_name is not None
                    ],
                )
                for builder in self
                if builder.report.table_name is not None
            ],
        )


metadata: Metadata = Metadata()