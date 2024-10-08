import json
from typing import Any, Iterable
from pyfuta.app.database import async_engine
from pyfuta.app.reports.models import ReportFragment, ReportFragmentType, ReportMixin
from sqlalchemy import text
from sqlmodel import Session
import re


async def sideload_mixins(mixins: Iterable[ReportMixin]):
    response = []
    async with async_engine.begin() as conn:
        for mixin in mixins:
            mixin_str = json.dumps(mixin.values)
            if mixin.sideload_sql is not None:
                result = await conn.execute(text(mixin.sideload_sql))
                result_tuple: tuple[str] = result.fetchone().tuple()
                for index, value in enumerate(result_tuple):
                    mixin_str = mixin_str.replace('"${' + str(index) + '}"', str(value) if type(value) == int else f'"{value}"')
            mixin.values = json.loads(mixin_str)
            response.append(mixin)
    return response


async def dispatch_statement(statement: str, parameters: dict, session: Session, report_id: int):
    sql_parameters = {}
    for trait in parameters.keys():
        frag = session.get(ReportFragment, (report_id, trait))
        if frag is not None and statement.find("$ { " + trait + " }") != -1:
            fragment = frag.sql
            if frag.type == ReportFragmentType.FILTER_SELECT:
                # replace the trait with the named fragment parameters.
                fragment = frag.sql.replace("${value}", f":{trait}")
                statement = statement.replace("$ { " + trait + " }", fragment)
                sql_parameters[trait] = parameters[trait]
            elif frag.type in [ReportFragmentType.FILTER_DATERANGE, ReportFragmentType.FILTER_DATEDAY, ReportFragmentType.FILTER_DATEMONTH]:
                for index, value in enumerate(parameters[trait].split(",")):
                    fragment = fragment.replace("${value" + str(index) + "}", f":{trait + str(index)}")
                    sql_parameters[trait + str(index)] = value
                statement = statement.replace("$ { " + trait + " }", fragment)
    statement = re.sub(r"\$\ \{\s*.*?\s*\}", "", statement)  # remove any remaining unused fragments
    async with async_engine.begin() as conn:
        # execute the statement with the replaced parameters.
        # the binding here is safe because we moved sanitized work to the sqlalchemy.
        result = await conn.execute(text(statement), sql_parameters)
        return result.fetchall()


async def dispatch_updating(table_name: str, field_name: str, nav_field_name: str, value: Any, nav_value: Any):
    value_dict = {"value": value, "nav_value": nav_value}
    statement = f"INSERT INTO {table_name} ({field_name}, {nav_field_name}) VALUES (:value, :nav_value) ON CONFLICT ({nav_field_name}) DO UPDATE SET {field_name}=:value"
    async with async_engine.begin() as conn:
        await conn.execute(text(statement), value_dict)


async def dispatch_inserting(table_name: str, data: dict[str, Any]):
    statement = f"INSERT INTO {table_name} ({','.join(data.keys())}) VALUES ({','.join([':' + key for key in data.keys()])})"
    async with async_engine.begin() as conn:
        await conn.execute(text(statement), data)


async def dispatch_deleting(table_name: str, pk_field: str, pk_value: Any):
    async with async_engine.begin() as conn:
        await conn.execute(text(f"DELETE FROM {table_name} WHERE {pk_field} = :value"), {"value": pk_value})
