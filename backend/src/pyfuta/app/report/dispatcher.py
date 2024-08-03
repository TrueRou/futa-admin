from typing import Any
from pyfuta.app.database import async_engine
from sqlalchemy import text


async def dispatch_statement(statement: str, parameters: dict):
    async with async_engine.begin() as conn:
        result = await conn.execute(text(statement), parameters)
        return result.fetchall()


async def dispatch_updating(table_name: str, field_name: str, nav_field_name: str, value: Any, nav_value: Any):
    clause_dict = {"table_name": table_name, "field_name": field_name, "nav_field_name": nav_field_name, "value": value, "nav_value": nav_value}
    async with async_engine.begin() as conn:
        result = await conn.execute(text(f"SELECT COUNT(*) FROM :table_name WHERE :nav_field_name=:nav_value"), clause_dict)
        if result.fetchone()[0] != 1:
            # This is a business rule, not a technical one
            # Might support batch update in the future because we have the dense navigation field
            raise ValueError("You can only update one row at a time, navigation must be unique")
        await conn.execute(text(f"UPDATE :table_name SET :field_name=:value WHERE :nav_field_name=:nav_value"), clause_dict)
