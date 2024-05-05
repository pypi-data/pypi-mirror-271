"""
Examples
--------
>>> import sqlexecx as db
>>> db.init('db.sqlite3', driver='sqlite3', debug=True)
>>> or
>>> db.init("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2', pool_size=5, debug=True)
>>> or
>>> db.init(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql')
>>> sql = 'INSERT INTO person(name, age) VALUES(?, ?)'
>>> db.execute(sql, '张三', 20)
1
>>> sql = 'SELECT id, name, age FROM person WHERE name=? and age=?'
>>> db.select(sql, '张三', 20)
[(3, '张三', 20)]
>>> db.insert('person', name='李四', age=18)
1
"""

from sqlexecutorx import (
    connection,
    transaction,
    with_connection,
    with_transaction,
    get_connection,
    close,
    Driver,
    Engine,
    init as _init
)
from .exec import (
    execute,
    insert,
    save,
    save_sql,
    save_select_key,
    save_sql_select_key,
    batch_insert,
    batch_execute,
    get,
    select,
    select_one,
    query,
    query_one,
    select_page,
    query_page,
    load,
    do_execute,
    do_save_sql,
    do_save_sql_select_key,
    do_get,
    do_select,
    do_select_one,
    do_query,
    do_query_one,
    do_select_page,
    do_query_page,
    do_load,
    insert_from_csv,
    insert_from_df,
    insert_from_json,
    truncate_table,
    drop_table,
    show_tables
)

from .sql_exec import sql
from .page_exec import page
from .table_exec import table
from .dialect import Dialect, Engine


def init(*args, **kwargs) -> Engine:
    """
    Compliant with the Python DB API 2.0 (PEP-249).

    Addition parameters:
    :param driver=None: str|Driver, import driver, 'import pymysql'
    :param pool_size=0: int, default 0, size of connection pool
    :param show_sql=False: bool,  if True, print sql
    :param debug=False: bool, if True, print debug context

    Other parameters of connection pool refer to DBUtils: https://webwareforpython.github.io/DBUtils/main.html#pooleddb-pooled-db

    Examples
    --------
    >>> import sqlexecx as db
    >>> db.init('db.sqlite3', driver='sqlite3', debug=True)
    >>> or
    >>> db.init("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2', pool_size=5, debug=True)
    >>> or
    >>> db.init(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql')
    """

    engine = _init(*args, **kwargs)
    Dialect.init(engine)
    return engine
