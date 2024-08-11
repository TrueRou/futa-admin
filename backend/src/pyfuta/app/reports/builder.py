from pyfuta.app import database
from pyfuta.app.reports.models import Report, ReportField, ReportFieldType, ReportType, ReportFragment
from sqlalchemy import Column, Table
from sqlmodel import SQLModel


class Field:
    def __init__(self, name: str, field_name: str = None, pk: bool = False):
        self.name = name
        self.field_name = field_name
        self.is_primary_key = pk


class Text(Field):
    def __init__(self, name: str, field_name: str = None, pk: bool = False):
        super().__init__(name, field_name, pk)
        self.type = ReportFieldType.TEXT


class Number(Field):
    def __init__(self, name: str, field_name: str = None, pk: bool = False):
        super().__init__(name, field_name, pk)
        self.type = ReportFieldType.NUMBER


class DateTime(Field):
    def __init__(self, name: str, field_name: str = None, pk: bool = False):
        super().__init__(name, field_name, pk)
        self.type = ReportFieldType.DATETIME


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
            self.report_fields.append(
                ReportField(
                    field_pos=self.field_pos, name=field.name, type=field.type, field_name=field.field_name, is_primary_key=field.is_primary_key
                )
            )
            self.field_pos += 1
        return self

    def chart(self, chart_type: ReportType, x_field: str, *y_field: str):
        self.report.type = chart_type
        self.fields(x_field, *[Number(field) for field in y_field])
        return self


class FragmentBuilder:
    def __init__(self, trait: str, sql: str, name: str, values: list[str]):
        self.fragment = ReportFragment(trait=trait, sql=sql, name=name, values=",".join(values))
        metadata.append(self)


class Metadata(list[ReportBuilder | FragmentBuilder]):
    async def create_all(self):
        import pyfuta.app.defs.reports  # noqa

        async with database.async_session_ctx() as session:
            for builder in self:
                if isinstance(builder, ReportBuilder):
                    session.add(builder.report)
                    await session.commit()  # This is necessary to get the id
                    await session.refresh(builder.report)
                    builder.report_id = builder.report.id
                    for field in builder.report_fields:
                        field.report_id = builder.report.id
                    session.add_all(builder.report_fields)
                elif isinstance(builder, FragmentBuilder):
                    session.add(builder.fragment)

            await session.commit()  # Apply the changes to all the transactions.

        SQLModel.metadata.create_all(
            database.engine,
            [
                Table(
                    builder.report.table_name,
                    SQLModel.metadata,
                    *[
                        Column(field.field_name, field.type.as_sqla(), primary_key=field.is_primary_key)
                        for field in builder.report_fields
                        if field.field_name is not None
                    ],
                )
                for builder in self
                if isinstance(builder, ReportBuilder) and builder.report.table_name is not None
            ],
        )


metadata: Metadata = Metadata()
