# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from configs.export import write_to_log
import traceback
import time
from configs.db import *

# 数据库操作

def exe_tidb(sql, args=None):
    #执行数据库操作
    conn = get_conn_sqldb()
    cur = conn.cursor()
    result_count = cur.execute(query=sql, args=args)
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return results, result_count

def select_tidb(sql, args=None):
    #数据库只读操作
    conn = get_conn_sqldb()
    cur = conn.cursor()
    result_count = cur.execute(query=sql, args=args)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results, result_count


def do_tidb_exe(sql, args=None, retrycount=5):
    try:
        results, result_count = exe_tidb(sql=sql, args=args)
        return results, result_count
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='db_op', defname='do_tidb_exe', result=sql+str(args)+error)
        if retrycount > 0:
            retrycount -= 1
            time.sleep(1)
            return do_tidb_exe(sql=sql, args=args, retrycount=retrycount)
        else:
            return 'sql_err', 0


def do_tidb_select(sql, args=None, retrycount=5):
    try:
        results, result_count = select_tidb(sql=sql, args=args)
        return results, result_count
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='db_op', defname='do_tidb_select', result=error)
        if retrycount > 0:
            retrycount -= 1
            time.sleep(1)
            return do_tidb_select(sql=sql, args=args, retrycount=retrycount)
        else:
            return 'sql_err', 0

if __name__ == "__main__":
    print(do_tidb_exe('show tables'))
