import pymysql
from app.utils.common import paginate_query, permission_exist, format_datetime
from app.utils.response import success_response, error_response
from connect import create_connection

# 创建权限
def create_permission(data):
    permission_name = data.get("permission_name")
    permission_value = data.get("permission_value")
    permission_type = data.get("permission_type")
    permission_uri = data.get("permission_uri", None)
    permission_icon = data.get("permission_icon", None)
    permission_pid = data.get("permission_pid", None)
    permission_status = data.get("permission_status", 1)  # 默认启用

    if not permission_name or not permission_value or permission_type is None:
        return error_response("权限名称、权限值和类型不能为空", 400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 校验权限值唯一
            cursor.execute("select permission_id from ums_permission where permission_value=%s", (permission_value,))
            if cursor.fetchone():
                return error_response("权限值已存在", 400)

            sql = """
                insert into ums_permission (permission_pid, permission_name, permission_value, permission_type,
                permission_uri, permission_icon, permission_status, permission_createdon)
                values (%s, %s, %s, %s, %s, %s, %s, now())
            """
            cursor.execute(sql, (permission_pid, permission_name, permission_value, permission_type,
                                 permission_uri, permission_icon, permission_status))
            conn.commit()
        return success_response("权限创建成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库错误: {str(e)}", 500)
    finally:
        conn.close()


# 修改权限
def update_permission(permission_id, data):
    if not permission_exist(permission_id):
        return error_response("权限不存在", 404)

    update_fields = []
    update_values = []

    if "permission_name" in data:
        update_fields.append("permission_name=%s")
        update_values.append(data["permission_name"])

    if "permission_value" in data:
        update_fields.append("permission_value=%s")
        update_values.append(data["permission_value"])

    if "permission_type" in data:
        update_fields.append("permission_type=%s")
        update_values.append(data["permission_type"])

    if "permission_uri" in data:
        update_fields.append("permission_uri=%s")
        update_values.append(data["permission_uri"])

    if "permission_icon" in data:
        update_fields.append("permission_icon=%s")
        update_values.append(data["permission_icon"])

    if "permission_status" in data:
        update_fields.append("permission_status=%s")
        update_values.append(data["permission_status"])

    if not update_fields:
        return error_response("没有需要更新的字段", 400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = f"update ums_permission set {', '.join(update_fields)} where permission_id=%s"
            update_values.append(permission_id)
            cursor.execute(sql, tuple(update_values))
            conn.commit()
        return success_response("权限信息已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库错误: {str(e)}", 500)
    finally:
        conn.close()


# 删除权限
def delete_permission(permission_id):
    if not permission_exist(permission_id):
        return error_response("权限不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 删除角色关联
            cursor.execute("delete from ums_role_permission where permission_id=%s", (permission_id,))
            # 删除权限
            cursor.execute("delete from ums_permission where permission_id=%s", (permission_id,))
            conn.commit()
        return success_response("权限已删除")
    except pymysql.MySQLError as e:
        return error_response(f"数据库错误: {str(e)}", 500)
    finally:
        conn.close()


# 分页查询权限
def list_permissions(keyword, page, page_size):
    offset, limit = paginate_query(page, page_size)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                select permission_id, permission_name, permission_value, permission_type, permission_uri, 
                permission_status, permission_createdon 
                from ums_permission 
                order by permission_createdon desc
                limit %s offset %s
            """
            cursor.execute(sql, (limit, offset))
            permissions = cursor.fetchall()

            cursor.execute("select count(*) as total from ums_permission")
            total = cursor.fetchone()["total"]

            for permission in permissions:
                permission["createdon"] = format_datetime(permission["createdon"])

        return success_response({"permissions": permissions, "total": total, "page": page, "page_size": page_size})
    except pymysql.MySQLError as e:
        return error_response(f"数据库错误: {str(e)}", 500)
    finally:
        conn.close()
