import pymysql
from connect import create_connection
from app.utils.common import validate_url, format_datetime
from app.utils.response import *

# 获取所有网站类型
def get_website_type():
    conn = create_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""select wt.*,coalesce(wtu.last_modified, wt.createdon) as last_modified
                                    from website_type wt
                                    left join website_type_update wtu on wt.type_id = wtu.type_id
                                    order by wt.createdon desc """)
            types = cursor.fetchall()
            for t in types:
                t["last_modified"] = format_datetime(t["last_modified"]) if t["last_modified"] else None
        return success_response(types, "获取网站类型成功",200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 添加网站类型
def add_type(type_name):
    if not type_name:
        return error_response("网站类型不能为空",400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("insert into website_type (type_name) values (%s)",(type_name,))
            conn.commit()
        return success_response("网站类型添加成功",200)
    except pymysql.IntegrityError:
        return error_response("该网站类型已存在",400)
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 删除网站类型
def delete_website_type(type_id):
    if not is_valid_type(type_id):
        return error_response("网站类型不存在",404)

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
        return success_response("网站类型及其关联网站已删除",200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}",500)
    finally:
        conn.close()

# 修改网站类型状态
def update_type_status(type_id, status):
    if status not in [0, 1]:
        return error_response("无效的状态值，应为 0 或 1", 400)

    if not is_valid_type(type_id):
        return error_response("网站类型不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("update website_type set status = %s where type_id = %s", (status, type_id))
            conn.commit()
        return success_response("网站类型状态更新成功", 200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 检查 type_id 是否存在
def is_valid_type(type_id):
    conn = create_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("select count(*) as count from website_type where type_id = %s", (type_id,))
            exist = cursor.fetchone()["count"] > 0
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
        return error_response("网址和网站类型不能为空",400)

    if not is_valid_type(type_id):
        return error_response(f"无效的网站类型 id: {type_id}",400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 处理换行符，拆分多个网站，并去除前后空格
            urls = [url.strip() for url in website_url.splitlines() if url.strip()]

            for url in urls:
                if not validate_url(url) and "*" not in url and ">" not in url:
                    return error_response(f"无效的网址格式: {url}",400)

            sql = "insert into website_content_control (website_url, type_id, status) values (%s, %s, %s)"
            values = [(url, type_id, status) for url in urls]
            cursor.executemany(sql, values)
            conn.commit()

        # 更新网站类型最后修改时间
        update_type_last_modified(type_id)

        return success_response("规则添加成功",200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}",500)
    finally:
        conn.close()

#   删除网站规则
def delete_website_rule(website_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("delete from  website_content_control where website_id = %s", (website_id,))
            conn.commit()
        return success_response("规则已删除",200)
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
        return success_response("规则状态已更新",200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}",500)
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

            for rule in rules:
                rule["website_url"] = rule["website_url"].replace("\r\n", "\n").replace("\r", "\n")

        return success_response(rules,"获取规则成功",200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}",500)
    finally:
        conn.close()

# 获取所有启用的 type_id（类型状态=1）
def get_enabled_type_ids():
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select type_id from website_type where status = 1")
            return [r[0] for r in cursor.fetchall()]
    finally:
        conn.close()

# 获取启用状态的网址规则，按类型分组返回
def get_enabled_type_url_map():
    conn = create_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                select type_id, website_url 
                from website_content_control 
                where status = 1
            """)
            mapping = {}
            for row in cursor.fetchall():
                tid = row["type_id"]
                mapping.setdefault(tid, []).append(row["website_url"])
            return mapping
    finally:
        conn.close()
