import pymysql
from app.utils.common import paginate_query, role_exist
from app.utils.response import success_response, error_response
from connect import create_connection

# 添加
def create_role(data):
    role_name = data.get("role_name")
    description = data.get("description", "")
    status = data.get("status", 1)
    if not role_name:
        return error_response("角色名称不能为空", 400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select role_id from ums_role where role_name=%s", (role_name,))
            if cursor.fetchone():
                return error_response("角色已存在", 400)

            sql = """
                insert into ums_role (role_name, description, status, createdon) 
                values (%s, %s, %s, NOW())
            """
            cursor.execute(sql, (role_name,description,status))
            conn.commit()
        return success_response("角色创建成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 编辑
def update_role(role_id, data):
    if not role_exist(role_id):
        return error_response("角色不存在", 404)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            update_fields = []
            update_values = []

            if "role_name" in data:
                cursor.execute("select role_id from ums_role where role_name=%s and role_id!=%s", (data["role_name"], role_id))
                if cursor.fetchone():
                    return error_response("角色名存在", 400)
                update_fields.append("role_name=%s")
                update_values.append(data["role_name"])

            if "description" in data:
                update_fields.append("description=%s")
                update_values.append(data["description"])

            if "status" in data:
                if data["status"] not in [0, 1]:
                    return error_response("状态值必须为 0（禁用）或 1（启用）", 400)
                update_fields.append("status = %s")
                update_values.append(data["status"])

            if not update_fields:
                return error_response("没有需要更新的字段", 400)

            sql = f"update ums_role set {', '.join(update_fields)} where role_id=%s"
            update_values.append(role_id)
            cursor.execute(sql, tuple(update_values))
            conn.commit()

            return success_response(message="角色信息已更新")

    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 删除
def remove_role(role_id):
    if not role_exist(role_id):
        return error_response("角色不存在", 404)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 删除该角色的用户关联
            cursor.execute("delete from  ums_user_role where role_id=%s", (role_id,))

            # 删除该角色的菜单关联
            cursor.execute("delete from ums_role_menu where role_id=%s", (role_id,))

            # 删除该角色的资源关联
            cursor.execute("delete from ums_role_resource where role_id=%s", (role_id,))

            # 删除该角色的权限关联
            cursor.execute("delete from ums_role_permission where role_id=%s", (role_id,))

            # 删除角色本身
            cursor.execute("delete from ums_role where role_id=%s", (role_id,))

            conn.commit()
            return success_response(message="角色已经删除")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 获取用户 模糊分页
def get_role_list(keyword, page, page_size):
    offset, limit = paginate_query(page, page_size)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                select r.role_id, r.role_name, r.description, r.status, r.createdon,
                       count(ur.user_id) as count
                from ums_role r
                left join ums_user_role ur on r.role_id = ur.role_id
                where r.role_name like %s
                group by r.role_id
                limit %s offset %s
            """
            cursor.execute(sql, (f"%{keyword}%", limit, offset))
            roles = cursor.fetchall()

            cursor.execute("select count(*) as total from ums_role where role_name like %s", (f"%{keyword}%",))
            total = cursor.fetchone()["total"]

        return success_response({"roles": roles, "total": total, "page": page, "page_size": page_size})
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 修改角色状态
def update_role_status(role_id, status):
    if not role_exist(role_id):
        return error_response("角色不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("update ums_role set status=%s where role_id=%s", (status, role_id))
            conn.commit()
        return success_response(message="角色状态已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 获取角色相关菜单
def get_role_menu(role_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select menu_id from ums_role_menu where role_id=%s", (role_id,))
            menu = cursor.fetchall()
        return success_response(menu, "获取角色菜单成功")
    finally:
        conn.close()

# 获取角色相关资源
def get_role_resource(role_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select resource_id from ums_role_resource where role_id=%s", (role_id,))
            resource = cursor.fetchall()
        return success_response(resource, "获取角色资源成功")
    finally:
        conn.close()

#  给角色分配菜单
def allocate_role_menu(role_id, menu_ids):
    if not role_exist(role_id):
        return error_response("角色不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 获取当前角色已有的菜单权限
            cursor.execute("select menu_id from ums_role_menu where role_id=%s", (role_id,))
            existing_menus = {row["menu_id"] for row in cursor.fetchall()}

            new_menus = set(menu_ids)

            # 需要删除的菜单
            menus_to_remove = existing_menus - new_menus
            # 需要新增的菜单
            menus_to_add = new_menus - existing_menus

            if menus_to_remove:
                sql = "delete from ums_role_menu where role_id=%s and menu_id in ({})".format(
                    ",".join(["%s"] * len(menus_to_remove))
                )
                cursor.execute(sql, [role_id] + list(menus_to_remove))

            if menus_to_add:
                sql = "insert into ums_role_menu (role_id, menu_id) values (%s, %s)"
                cursor.executemany(sql, [(role_id, menu_id) for menu_id in menus_to_add])

            conn.commit()
        return success_response("角色菜单已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 给角色分配资源
def allocate_role_resource(role_id, resource_ids):
    if not role_exist(role_id):
        return error_response("角色不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 获取当前角色已有的资源权限
            cursor.execute("select resource_id from ums_role_resource where role_id=%s", (role_id,))
            existing_resources = {row["resource_id"] for row in cursor.fetchall()}

            new_resources = set(resource_ids)

            # 需要删除的资源
            resources_to_remove = existing_resources - new_resources
            # 需要新增的资源
            resources_to_add = new_resources - existing_resources

            if resources_to_remove:
                sql = "delete from ums_role_resource where role_id=%s and resource_id in ({})".format(
                    ",".join(["%s"] * len(resources_to_remove))
                )
                cursor.execute(sql, [role_id] + list(resources_to_remove))

            if resources_to_add:
                sql = "insert into ums_role_resource (role_id, resource_id) values (%s, %s)"
                cursor.executemany(sql, [(role_id, resource_id) for resource_id in resources_to_add])

            conn.commit()
        return success_response("角色资源已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 获取角色权限

def get_role_permission(role_id):
    if not role_exist(role_id):
        return error_response("角色不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                select p.permission_id, p.permission_name, p.permission_value, p.permission_type
                from ums_permission p
                join ums_role_permission rp on p.permission_id = rp.permission_id
                where rp.role_id = %s
            """
            cursor.execute(sql, (role_id,))
            permissions = cursor.fetchall()

        return success_response(permissions, "获取角色权限成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 给角色分配权限（增量更新）
def allocate_role_permission(role_id, permission_ids):
    if not role_exist(role_id):
        return error_response("角色不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 获取当前角色已有的权限
            cursor.execute("select permission_id from ums_role_permission where role_id=%s", (role_id,))
            existing_permissions = {row["permission_id"] for row in cursor.fetchall()}

            new_permissions = set(permission_ids)

            # 需要删除的权限
            permissions_to_remove = existing_permissions - new_permissions
            # 需要新增的权限
            permissions_to_add = new_permissions - existing_permissions

            if permissions_to_remove:
                sql = "delete from ums_role_permission where role_id=%s and permission_id in ({})".format(
                    ",".join(["%s"] * len(permissions_to_remove))
                )
                cursor.execute(sql, [role_id] + list(permissions_to_remove))

            if permissions_to_add:
                sql = "insert into ums_role_permission (role_id, permission_id) values (%s, %s)"
                cursor.executemany(sql, [(role_id, permission_id) for permission_id in permissions_to_add])

            conn.commit()
        return success_response("角色权限已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()
