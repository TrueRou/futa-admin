from pyfuta.app.database import session_ctx
from pyfuta.app.report.builder import ReportBuilder

with session_ctx() as session:
    ReportBuilder("Users", "SELECT * FROM users", ["id", "name", "email", "created_at", "updated_at"]).build(session)
