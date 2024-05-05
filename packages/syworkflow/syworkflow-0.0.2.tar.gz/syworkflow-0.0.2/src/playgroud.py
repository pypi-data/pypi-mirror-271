import logging
import sqlite3

import syworkflow as wf

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s - '
    '%(name)s.%(funcName)s(%(lineno)s) '
    '[%(processName)s]<%(threadName)s>'
    ': %(message)s',
    level=logging.DEBUG)


def connect_fn():
  conn = sqlite3.connect(":memory:", autocommit=True)
  return conn


if __name__ == '__main__':
  sql = """
    create table if not exists test(
      name   string,
      value  bigint
    );

    insert into test (name, value)
    values ('a', 1), ('b', 2)
    ;
    """
  task = wf.SQLExecutionTask(connect_fn=connect_fn, sql_statement=sql)
  schd = wf.TaskScheduler()
  schd.add_task(task)
  schd.start()
