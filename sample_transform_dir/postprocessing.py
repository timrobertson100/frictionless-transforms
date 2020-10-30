import sqlalchemy


def _field_in_table(connection: sqlalchemy.engine.base.Connection, table_name: str, field_name: str) -> bool:
    """Return true if a field already exists in a given table."""
    sql = f"select count(*) from pragma_table_info('{table_name}') where name='{field_name}';"
    result = connection.execute(sql)
    return result.first().values()[0] == 1


def _add_field_if_not_exists(connection: sqlalchemy.engine.base.Connection,
                             table_name: str,
                             field_name: str,
                             field_description: str):
    if not _field_in_table(connection, table_name, field_name):
        sql = f"ALTER TABLE {table_name} ADD {field_name} {field_description};"
        connection.execute(sql)


def postprocess_database(connection: sqlalchemy.engine.base.Connection):
    _add_field_if_not_exists(connection, "data", "new_field", "CHAR(50)")