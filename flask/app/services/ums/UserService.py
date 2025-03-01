import pymysql

from app.utils.common import paginate_query, hash_pwd, user_exist, role_exist, format_datetime
from connect import create_connection
from app.utils.response import *


#获取用户列表，分页
def get_users(page, per_page, search):
    offset, per_page = paginate_query(page, per_page)
    search = search.strip()  #去除空格
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                select user_id, username, fullname, status, createdon, lastlogin, status
                from ums_user
                where lower(username) like lower(%s) or lower(fullname) like lower(%s)
                limit %s offset %s
            """
            cursor.execute(sql, (f"%{search}%", f"%{search}%", per_page, offset))
            users = cursor.fetchall()

            cursor.execute("select count(*) as count from ums_user where username like %s or fullname like %s",(f"%{search}%", f"%{search}%"))
            total = cursor.fetchone()["count"]

            for user in users:
                user["createdon"] = format_datetime(user["createdon"])
                user["lastlogin"] = format_datetime(user["lastlogin"])
        return success_response({"users": users, "total": total, "page": page, "per_page": per_page})
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 添加用户
def create_user(data):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select user_id from ums_user where username=%s", (data["username"],))
            if cursor.fetchone():
                return error_response("用户已存在",400)

            sql = """
                insert into ums_user(username,fullname,password, status, createdon)
                values (%s,%s,%s,%s,now())
            """
            cursor.execute(sql, (data["username"],data["fullname"],hash_pwd(data["password"]),data["status"]))
            conn.commit()
            return success_response(message="用户创建成功")

    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 编辑用户
def update_user(user_id, data):
    if not user_exist(user_id):
        return error_response("用户不存在", 404)

    conn = create_connection()

    try:
        with conn.cursor() as cursor:
            update_fields = []
            update_values = []

            if "username" in data:
                cursor.execute("select user_id from ums_user where username=%s and user_id!=%s", (data["username"], user_id))
                # 用户名唯一
                if cursor.fetchone():
                    return error_response("用户名已存在", 400)
                update_fields.append("username=%s")
                update_values.append(data["username"])

            if "fullname" in data:
                update_fields.append("fullname=%s")
                update_values.append(data["fullname"])

            if "password" in data:
                update_fields.append("password = %s")
                update_values.append(hash_pwd(data["password"]))

            if "status" in data:
                if data["status"] not in [0, 1]:
                    return error_response("状态值必须为 0（禁用）或 1（启用）", 400)
                update_fields.append("status = %s")
                update_values.append(data["status"])

            if not update_fields:
                return error_response("没有需要更新的字段", 400)

            sql = f"UPDATE ums_user SET {', '.join(update_fields)} WHERE user_id=%s"
            update_values.append(user_id)
            cursor.execute(sql, tuple(update_values))
            conn.commit()

            return success_response(message="用户信息已更新")

    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 删除用户
def delete_user(user_id):
    if not user_exist(user_id):
        return error_response("用户不存在", 404)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("delete from ums_user_role where user_id=%s", (user_id,))
            cursor.execute("delete from ums_user where user_id=%s", (user_id,))
            conn.commit()
            return success_response(message="用户已经删除")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 启用/禁用
def toggle_user_status(user_id, status):
    if not user_exist(user_id):
        return error_response("用户不存在", 404)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = "update ums_user set status=%s where user_id=%s"
            cursor.execute(sql,(status,user_id))
            conn.commit()
            return success_response(message="用户状态已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 分配角色
def assign_user_role(user_id, role_ids):
    if not user_exist(user_id):
        return error_response("用户不存在", 404)
    for role_id in role_ids:
        if not role_exist(role_id):
            return error_response("角色不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = "delete from ums_user_role where user_id=%s"
            cursor.execute(sql,(user_id,))
            sql2 = "insert into ums_user_role (user_id, role_id) values (%s, %s)"
            cursor.executemany(sql2, [(user_id, role_id) for role_id in role_ids])

            conn.commit()
            return success_response(message="用户角色分配成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()