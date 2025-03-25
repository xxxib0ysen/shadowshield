import pymysql
from connect import create_connection
from app.utils.response import *
from app.utils.common import validate_url, format_datetime

# 获取所有自定义规则
def get_custom_rules():
    conn = create_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("select * from custom_website_rule order by createdon desc")
            rules = cursor.fetchall()
            for r in rules:
                r["createdon"] = format_datetime(r["createdon"])
            return success_response(rules, "获取自定义规则成功", 200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()


# 添加规则（支持批量导入，支持 *、>）
def add_custom_rules(data):
    website_urls = data.get("website_url", "").strip()
    status = data.get("status", 0)

    if not website_urls:
        return error_response("请输入要控制的网站", 400)

    conn = create_connection()
    try:
        urls = [u.strip() for u in website_urls.splitlines() if u.strip()]
        for url in urls:
            if not validate_url(url) and "*" not in url and ">" not in url:
                return error_response(f"无效的网址格式: {url}", 400)

        with conn.cursor() as cursor:
            sql = "insert into custom_website_rule (website_url, status) values (%s, %s)"
            values = [(url, status) for url in urls]
            cursor.executemany(sql, values)
            conn.commit()

        return success_response("自定义规则添加成功", 200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库插入失败: {str(e)}", 500)
    finally:
        conn.close()


# 启用/禁用规则
def update_custom_rule_status(rule_id, status):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("update custom_website_rule set status = %s where id = %s", (status, rule_id))
            conn.commit()
        return success_response("规则状态更新成功", 200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 获取所有启用状态的规则（供代理层调用）
def get_enabled_custom_rules():
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select website_url from custom_website_rule where status = 1")
            rows = cursor.fetchall()
            return [r[0] for r in rows]
    finally:
        conn.close()

# 删除单个规则
def delete_custom_rule(rule_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("delete from custom_website_rule where id = %s", (rule_id,))
            conn.commit()
        return success_response("规则删除成功", 200)
    except pymysql.MySQLError as e:
        return error_response(f"数据库删除失败: {str(e)}", 500)
    finally:
        conn.close()


# 批量删除
def delete_custom_rule_batch(ids):
    if not ids:
        return error_response("未提供要删除的规则 ID", 400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            format_strings = ','.join(['%s'] * len(ids))
            sql = f"delete from custom_website_rule where id in ({format_strings})"
            cursor.execute(sql, ids)
            conn.commit()
        return success_response("批量删除成功", 200)
    except pymysql.MySQLError as e:
        return error_response(f"批量删除失败: {str(e)}", 500)
    finally:
        conn.close()

