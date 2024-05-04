"""
Examples
--------
>>> import sqlexecutorx as db
>>> db.init('db.sqlite3', driver='sqlite3', debug=True)
>>> or
>>> db.init("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2', pool_size=5, debug=True)
>>> or
>>> db.init(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql')
>>> sql = 'insert into person(name, age) values(%s, %s)'
>>> db.execute(sql, '张三', 20)
1
>>> sql = 'SELECT id, name, age FROM person WHERE name=%s and age=%s'
>>> db.select(sql, '张三', 20)
[(3, '张三', 20)]
"""

from .core import (
    init,
    connection,
    transaction,
    with_connection,
    with_transaction,
    get_connection,
    close,
    execute,
    save,
    get,
    select,
    select_one,
    query,
    query_one,
    do_select,
    do_select_one,
    batch_execute
)
from .support import DBError, Dict
from .engine import Engine, Driver
