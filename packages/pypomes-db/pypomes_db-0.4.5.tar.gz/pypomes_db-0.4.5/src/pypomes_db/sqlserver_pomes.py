from logging import Logger
from pyodbc import connect, Connection, Row

from .db_common import (
    _assert_query_quota, _db_get_params, _db_log, _db_except_msg
)


def db_connect(errors: list[str],
               logger: Logger = None) -> Connection:
    """
    Obtain and return a connection to the database, or *None* if the connection could not be obtained.

    :param errors: incidental error messages
    :param logger: optional logger
    :return: the connection to the database
    """
    # initialize the return valiable
    result: Connection | None = None

    # obtain the connection string
    connection_kwargs: str = _get_connection_kwargs()

    # Obtain a connection to the database
    err_msg: str | None = None
    try:
        result = connect(connection_kwargs)
    except Exception as e:
        err_msg = _db_except_msg(exception=e,
                                 engine="sqlserver")

    # log the results
    name, _user, _pwd, host, _port = _db_get_params("sqlserver")
    _db_log(errors=errors,
            err_msg=err_msg,
            logger=logger,
            query_stmt=f"Connecting to '{name}' at '{host}'")

    return result


def db_select_all(errors: list[str],
                  sel_stmt: str,
                  where_vals: tuple = None,
                  require_min: int = None,
                  require_max: int = None,
                  logger: Logger = None) -> list[tuple]:
    """
    Search the database and return all tuples that satisfy the *sel_stmt* search command.

    The command can optionally contain search criteria, with respective values given
    in *where_vals*. The list of values for an attribute with the *IN* clause must be contained
    in a specific tuple. If not positive integers, *require_min* and *require_max* are ignored.
    If the search is empty, an empty list is returned.

    :param errors: incidental error messages
    :param sel_stmt: SELECT command for the search
    :param where_vals: the values to be associated with the search criteria
    :param require_min: optionally defines the minimum number of tuples to be returned
    :param require_max: optionally defines the maximum number of tuples to be returned
    :param logger: optional logger
    :return: list of tuples containing the search result, or [] if the search is empty
    """
    # initialize the return variable
    result: list[tuple] = []

    # obtain the connection string
    connection_kwargs: str = _get_connection_kwargs()

    err_msg: str | None = None
    if isinstance(require_max, int) and require_max > 0:
        sel_stmt: str = sel_stmt.replace("SELECT", f"SELECT TOP {require_max}", 1)

    try:
        # obtain a connection
        with connect(connection_kwargs) as conn:
            # make sure the connection is not in autocommit mode
            conn.autocommit = False

            # obtain a cursor and execute the operation
            with conn.cursor() as cursor:
                cursor.execute(sel_stmt, where_vals)
                # obtain the number of tuples returned
                count: int = cursor.rowcount

                # has the query quota been satisfied ?
                if _assert_query_quota(errors=errors,
                                       query=sel_stmt,
                                       where_vals=where_vals,
                                       count=count,
                                       require_min=require_min,
                                       require_max=require_max):
                    # yes, retrieve the returned tuples
                    rows: list[Row] = cursor.fetchall()
                    result = [tuple(row) for row in rows]
            # commit the transaction
            conn.commit()
    except Exception as e:
        err_msg = _db_except_msg(exception=e,
                                 engine="sqlserver")

    # log the results
    _db_log(errors=errors,
            err_msg=err_msg,
            logger=logger,
            query_stmt=sel_stmt,
            bind_vals=where_vals)

    return result


def db_bulk_insert(errors: list[str],
                   insert_stmt: str,
                   insert_vals: list[tuple],
                   logger: Logger = None) -> int:
    """
    Insert the tuples, with values defined in *insert_vals*, into the database.

    :param errors: incidental error messages
    :param insert_stmt: the INSERT command
    :param insert_vals: the list of values to be inserted
    :param logger: optional logger
    :return: the number of inserted tuples, or None if an error occurred
    """
    # initialize the return variable
    result: int | None = None

    # obtain the connection string
    connection_kwargs: str = _get_connection_kwargs()

    err_msg: str | None = None
    try:
        # obtain a connection
        with connect(connection_kwargs) as conn:
            # make sure the connection is not in autocommit mode
            conn.autocommit = False

            # obtain the cursor and perform the operation
            with conn.cursor() as cursor:
                cursor.fast_executemany = True
                try:
                    cursor.executemany(insert_stmt, insert_vals)
                    result = len(insert_vals)
                except Exception:
                    conn.rollback()
                    raise
            conn.commit()
    except Exception as e:
        err_msg = _db_except_msg(exception=e,
                                 engine="sqlserver")

    # log the results
    _db_log(errors=errors,
            err_msg=err_msg,
            logger=logger,
            query_stmt=insert_stmt,
            bind_vals=insert_vals[0])

    return result


def db_execute(errors: list[str],
               exc_stmt: str,
               bind_vals: tuple,
               logger: Logger) -> int:
    """
    Execute the command *exc_stmt* on the database.

    This command might be a DML ccommand modifying the database, such as
    inserting, updating or deleting tuples, or it might be a DDL statement,
    or it might even be an environment-related command.
    The optional bind values for this operation are in *bind_vals*.
    The value returned is the value obtained from the execution of *exc_stmt*.
    It might be the number of inserted, modified, or deleted tuples,
    ou None if an error occurred.

    :param errors: incidental error messages
    :param exc_stmt: the command to execute
    :param bind_vals: optional bind values
    :param logger: optional logger
    :return: the return value from the command execution
    """
    # initialize the return variable
    result: int | None = None

    # obtain the connection string
    connection_kwargs: str = _get_connection_kwargs()

    err_msg: str | None = None
    try:
        # obtain a connection
        with connect(connection_kwargs) as conn:
            # make sure the connection is not in autocommit mode
            conn.autocommit = False
            # obtain the cursor and execute the operation
            with conn.cursor() as cursor:
                cursor.execute(exc_stmt, bind_vals)
                result = cursor.rowcount
            # commit the transaction
            conn.commit()
    except Exception as e:
        err_msg = _db_except_msg(exception=e,
                                 engine="sqlserver")

    # log the results
    _db_log(errors=errors,
            err_msg=err_msg,
            logger=logger,
            query_stmt=exc_stmt,
            bind_vals=bind_vals)

    return result


def db_call_procedure(errors: list[str],
                      proc_name: str,
                      proc_vals: tuple,
                      require_min: int = None,
                      require_max: int = None,
                      logger: Logger = None) -> list[tuple]:
    """
    Execute the stored procedure *proc_name* in the database, with the parameters given in *proc_vals*.

    :param errors: incidental error messages
    :param proc_name: name of the stored procedure
    :param proc_vals: parameters for the stored procedure
    :param require_min: optionally defines the minimum number of tuples to be returned
    :param require_max: optionally defines the maximum number of tuples to be returned
    :param logger: optional logger
    :return: the data returned by the procedure
    """
    # initialize the return variable
    result: list[tuple] | None = None

    # obtain the connection string
    connection_kwargs: str = _get_connection_kwargs()

    # build the command
    proc_stmt: str | None = None

    # execute the stored procedure
    err_msg: str | None = None
    try:
        # obtain a connection
        with connect(connection_kwargs) as conn:
            # make sure the connection is not in autocommit mode
            conn.autocommit = False
            # obtain the cursor and execute the operation
            with conn.cursor() as cursor:
                proc_stmt = f"SET NOCOUNT ON; EXEC {proc_name} {','.join(('?',) * len(proc_vals))}"
                cursor.execute(proc_stmt, proc_vals)
                # obtain the number of tuples returned
                count: int = cursor.rowcount

                # has the query quota been satisfied ?
                # noinspection PyTypeChecker
                if _assert_query_quota(errors, proc_name, None, count, require_min, require_max):
                    # yes, retrieve the returned tuples
                    rows: list[Row] = cursor.fetchall()
                    result = [tuple(row) for row in rows]
            # commit the transaction
            conn.commit()
    except Exception as e:
        err_msg = _db_except_msg(exception=e,
                                 engine="sqlserver")

    # log the results
    _db_log(errors=errors,
            err_msg=err_msg,
            logger=logger,
            query_stmt=proc_stmt,
            bind_vals=proc_vals)

    return result


def _get_connection_kwargs() -> str:

    # retrieve the connection parameters
    name, user, pwd, host, port, driver = _db_get_params("sqlserver")
    return (
        f"DRIVER={{{driver}}};SERVER={host},{port};"
        f"DATABASE={name};UID={user};PWD={pwd};TrustServerCertificate=yes;"
    )
