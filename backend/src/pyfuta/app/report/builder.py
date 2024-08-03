from pyfuta.app import database
from pyfuta.app.report.models import Report, ReportField, ReportFieldType
from sqlmodel import Session


class F:
    def __init__(self, name: str, type: ReportFieldType = ReportFieldType.NUMBER):
        self.name = name
        self.type = type


class ReportBuilder:
    field_pos: int = 0
    report_fields: list[ReportField] = []

    def __init__(self, name: str, sql: str, fields: list[str | F]):
        self.report = Report(name=name, sql=sql)
        for field in fields:
            field = F(name=field) if isinstance(field, str) else field
            self.report_fields.append(ReportField(field_pos=self.field_pos, name=field.name, type=field.type))
            self.field_pos += 1

    def build(self, session: Session) -> Report:
        database.add_model(session, self.report)
        for field in self.report_fields:
            field.report_id = self.report.id
        session.add_all(self.report_fields)
        session.commit()
        return self.report
