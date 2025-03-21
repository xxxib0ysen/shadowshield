import pymysql
from connect import create_connection
from app.utils.common import validate_url
from app.utils.response import *

# 获取所有网站类型
def get_website_type():
    conn = create_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("select * from website_type order by createdon desc ")
            types = cursor.fetchall()
        return success_response(types)
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 添加网站类型
def add_type(type_name):
    if not type_name:
        return error_response("网站类型不能为空")

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("insert into website_type (type_name) values (%s)",(type_name,))
            conn.commit()
        return success_response("网站类型添加成功")
    except pymysql.IntegrityError:
        return error_response("该网站类型已存在")
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 删除网站类型
def delete_website_type(type_id):
    if not is_valid_type(type_id):
        return error_response("网站类型不存在")

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 删除该类型下的所有网站
            cursor.execute("delete from website_content_control where type_id = %s", (type_id,))
            # 删除website_type_update记录
            cursor.execute("delete from website_type_update where type_id = %s", (type_id,))
            # 删除类型
            cursor.execute("delete from website_type where type_id = %s", (type_id,))
            conn.commit()
        return success_response("网站类型及其关联网站已删除")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}")
    finally:
        conn.close()

# 检查 type_id 是否存在
def is_valid_type(type_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select count(*) from website_type where type_id = %s", (type_id,))
            exist = cursor.fetchone()[0] > 0
        return exist
    finally:
        conn.close()

# 更新 website_type_update 的 last_modified
def update_type_last_modified(type_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            insert into  website_type_update (type_id, last_modified) 
            values (%s, now()) 
            on duplicate key update last_modified = now()
            """
            cursor.execute(sql, (type_id,))
            conn.commit()
    finally:
        conn.close()

# 添加网站访问规则，支持批量添加
def add_website_rule(data):
    website_url = data.get("website_url", "").strip()
    type_id = data.get("type_id")
    status = data.get("status", 1)

    if not website_url or not type_id:
        return error_response("网址和网站类型不能为空")

    if not is_valid_type(type_id):
        return error_response(f"无效的网站类型 id: {type_id}")

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 处理换行符，拆分多个网站，并去除前后空格
            urls = [url.strip() for url in website_url.split("\n") if url.strip()]

            for url in urls:
                if not validate_url(url):
                    return error_response(f"无效的网址格式: {url}")

            sql = "insert into website_content_control (website_url, type_id, status) values (%s, %s, %s)"
            values = [(url, type_id, status) for url in urls]
            cursor.executemany(sql, values)
            conn.commit()

        # 更新网站类型最后修改时间
        update_type_last_modified(type_id)

        return success_response("规则添加成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}")
    finally:
        conn.close()

#   删除网站规则
def delete_website_rule(website_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("delete from  website_content_control where website_id = %s", (website_id,))
            conn.commit()
        return success_response("规则已删除")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 启用/禁用
def update_website_status(website_id, status):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = "update website_content_control set status = %s where website_id = %s"
            cursor.execute(sql, (status, website_id))
            conn.commit()
        return success_response("规则状态已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}")
    finally:
        conn.close()

# 获取所有规则
def get_website_rule():
    conn = create_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                select wc.website_id, wc.website_url, wt.type_name, wc.status, wc.createdon 
                from website_content_control wc 
                join website_type wt on wc.type_id = wt.type_id
                order by  wc.createdon desc
            """)
            rules = cursor.fetchall()
        return success_response(rules)
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}")
    finally:
        conn.close()