from typing import Any
from pyfuta.app.database import async_engine
from sqlalchemy import text


async def dispatch_statement(statement: str, parameters: dict):
    async with async_engine.begin() as conn:
        result = await conn.execute(text(statement), parameters)
        return result.fetchall()


async def dispatch_updating(table_name: str, field_name: str, nav_field_name: str, value_dict: Any, nav_value: Any):
    value_dict = {"value": value_dict, "nav_value": nav_value}
    async with async_engine.begin() as conn:
        await conn.execute(text(f"UPDATE {table_name} SET {field_name}=:value WHERE {nav_field_name}=:nav_value"), value_dict)
