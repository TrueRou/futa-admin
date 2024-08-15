import json
from pyfuta.app import database
from pyfuta.app.reports.models import Report, ReportField, ReportFieldType, ReportFragmentType, ReportMixin, ReportType, ReportFragment
from sqlalchemy import Column, Table
from sqlmodel import SQLModel


class Field:
    def __init__(self, name: str, field_name: str = None, pk: bool = False):
        self.field = ReportField(name=name, field_name=field_name, is_primary_key=pk)


class Text(Field):
    def __init__(self, name: str, field_name: str = None, pk: bool = False):
        super().__init__(name, field_name, pk)
        self.field.type = ReportFieldType.TEXT


class Number(Field):
    def __init__(self, name: str, field_name: str = None, pk: bool = False):
        super().__init__(name, field_name, pk)
        self.field.type = ReportFieldType.NUMBER


class DateTime(Field):
    def __init__(self, name: str, field_name: str = None, pk: bool = False):
        super().__init__(name, field_name, pk)
        self.field.type = ReportFieldType.DATETIME


class Fragment:
    def __init__(self, trait: str, sql: str, name: str, type: ReportFragmentType, values: list[str] = None):
        self.fragment = ReportFragment(trait=trait, sql=sql, name=name, type=type, values=",".join(values) if values else None)


class Mixin:
    def __init__(self, ref_variable: str, values: str):
        dictionary = json.loads(values)  # Ensure it is a valid json
        self.mixin = ReportMixin(ref_variable=ref_variable, values=dictionary)


class ReportBuilder:
    def __init__(self, name: str, sql: str, table_name: str = None):
        self.report = Report(name=name, sql=sql, table_name=table_name)
        self.field_pos: int = 0
        self.report_id: int = -1
        self.report_fields: list[ReportField] = []
        self.report_fragments: list[ReportFragment] = []
        self.report_mixins: list[ReportMixin] = []
        metadata.append(self)

    def chart(self, chart_type: ReportType, x_field: str, *y_field: str):
        self.report.type = chart_type
        self.fields(x_field, *[Number(field) for field in y_field])
        return self

    def fields(self, *fields: str | Text | Number):
        for field in fields:
            field = Text(name=field) if isinstance(field, str) else field
            field.field.field_pos = self.field_pos
            self.report_fields.append(field.field)
            self.field_pos += 1
        return self

    def fragments(self, *fragments: Fragment):
        for fragment in fragments:
            self.report_fragments.append(fragment.fragment)
        return self

    def mixins(self, *mixins: Mixin):
        for mixin in mixins:
            self.report_mixins.append(mixin.mixin)
        return self


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
                for fragment in builder.report_fragments:
                    fragment.report_id = builder.report.id
                for mixin in builder.report_mixins:
                    mixin.report_id = builder.report.id
                session.add_all(builder.report_fields)
                session.add_all(builder.report_fragments)
                session.add_all(builder.report_mixins)

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
