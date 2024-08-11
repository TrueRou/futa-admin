from typing import Any
from pyfuta.app.database import async_engine
from pyfuta.app.reports.models import ReportFragment
from sqlalchemy import text
from sqlmodel import Session
import re


async def dispatch_statement(statement: str, parameters: dict, session: Session):
    for locator_key in parameters.keys():
        frag = session.get(ReportFragment, locator_key)
        if frag is not None and statement.find("${" + locator_key + "}") != -1:
            # replace the locator with the named fragment parameters.
            fragment = frag.sql.replace("${value}", f":{locator_key}")
            statement = statement.replace("${" + locator_key + "}", fragment)
    statement = re.sub(r"\${.*?}", "", statement)  # remove any remaining unused fragments
    async with async_engine.begin() as conn:
        # execute the statement with the replaced parameters.
        # the binding here is safe because we moved sanitized work to the sqlalchemy.
        result = await conn.execute(text(statement), parameters)
        return result.fetchall()


async def dispatch_updating(table_name: str, field_name: str, nav_field_name: str, value: Any, nav_value: Any):
    value_dict = {"value": value, "nav_value": nav_value}
    async with async_engine.begin() as conn:
        await conn.execute(text(f"UPDATE {table_name} SET {field_name}=:value WHERE {nav_field_name}=:nav_value"), value_dict)
