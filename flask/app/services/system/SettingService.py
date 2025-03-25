import pymysql

from connect import create_connection
# 获取某个设置项的值
def get_setting(key):
    conn = create_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("select value from system_setting where `key` = %s", (key,))
            result = cursor.fetchone()
            return result['value'] if result else None
    finally:
        conn.close()

# 设置某个设置项（存在则更新）
def set_setting(key, value):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                insert into system_setting (`key`, `value`) 
                values (%s, %s) 
                on duplicate key update `value` = values(`value`)
            """, (key, value))
            conn.commit()
    finally:
        conn.close()

# 判断是否启用了网站访问限制功能
def is_website_blocking_enabled():
    return get_setting("website_blocking_enabled") == "1"