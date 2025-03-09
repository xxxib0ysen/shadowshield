import pymysql
from app.utils.response import *
from app.utils.common import *
from connect import *

#添加
def create_menu(data):
    title = data.get("title")
    name = data.get("name")
    icon = data.get("icon")
    menu_pid = data.get("menu_pid",None)
    hidden = data.get("hidden",0)

    if not title or not name:
        return error_response("菜单名称和前端路由名称不能为空",400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            #校验唯一
            cursor.execute("select menu_id from ums_menu where title=%s or name=%s", (title, name))
            if cursor.fetchone():
                return error_response("菜单名称或前端路由名称已存在",400)

            # 计算菜单层级
            level = 1
            if menu_pid:
                if not menu_exist(menu_pid):
                    return error_response("父级菜单不存在", 404)

                cursor.execute("select level from ums_menu where menu_id=%s", (menu_pid,))
                parent = cursor.fetchone()
                if parent:
                    level = parent["level"] + 1

            sql = """
                    insert into ums_menu (menu_pid, title, name, icon, hidden, level, createdon)
                    values (%s, %s, %s, %s, %s, %s, now())
                """
            cursor.execute(sql, (menu_pid, title, name, icon, hidden, level))
            conn.commit()

        return success_response("菜单创建成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 修改菜单
def update_menu(menu_id, data):
    if not menu_exist(menu_id):
        return error_response("菜单不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            update_fields = []
            update_values = []

            if "title" in data or "name" in data:
                title = data.get("title","")
                name = data.get("name","")

                cursor.execute("select menu_id from ums_menu where (title=%s or name=%s) and menu_id!=%s", (title, name, menu_id))
                if cursor.fetchone():
                    return error_response("菜单名称或路由名称已存在", 400)

            if "title" in data:
                update_fields.append("title=%s")
                update_values.append(data["title"])

            if "name" in data:
                update_fields.append("name=%s")
                update_values.append(data["name"])

            if "icon" in data:
                update_fields.append("icon=%s")
                update_values.append(data["icon"])

            if "hidden" in data:
                update_fields.append("hidden=%s")
                update_values.append(data["hidden"])

            # menu_pid 更新，并自动更新 level
            if "menu_pid" in data:
                menu_pid = data["menu_pid"]
                if menu_pid:  # 有父级菜单
                    if not menu_exist(menu_pid):
                        return error_response("父级菜单不存在", 404)
                    cursor.execute("select level from ums_menu where menu_id=%s", (menu_pid,))
                    parent = cursor.fetchone()
                    level = parent["level"] + 1 if parent else 1
                else:  # 无父级菜单，设为一级菜单
                    menu_pid = None
                    level = 1

                update_fields.append("menu_pid=%s")
                update_values.append(menu_pid)

                update_fields.append("level=%s")
                update_values.append(level)

            if not update_fields:
                return error_response("没有需要更新的字段", 400)

            sql = f"update ums_menu set {', '.join(update_fields)} where menu_id=%s"
            update_values.append(menu_id)
            cursor.execute(sql, tuple(update_values))
            conn.commit()
        return success_response("菜单信息已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 获取所有菜单 分页
def get_all_menu(page,page_size,level=None):
    offset, limit = paginate_query(page, page_size)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            if level:  # level筛选
                cursor.execute("""
                        select SQL_CALC_FOUND_ROWS * from ums_menu 
                        where level=%s 
                        order by level asc, menu_id asc limit %s offset %s
                    """, (level, limit, offset))
            else:
                cursor.execute("""
                        select SQL_CALC_FOUND_ROWS * from ums_menu 
                        order by level asc, menu_id asc limit %s offset %s
                    """, (limit, offset))

            menus = cursor.fetchall()
            cursor.execute("select FOUND_ROWS() as total")
            total = cursor.fetchone()["total"]
            for menu in menus:
                menu["createdon"] = format_datetime(menu["createdon"])
        return success_response({
            "menus": menus,
            "total": total,
            "page": page,
            "page_size": page_size
        }, "获取菜单成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 删除菜单
def remove_menu(menu_id):
    if not menu_exist(menu_id):
        return error_response("菜单不存在", 404)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 检查是否有子菜单
            cursor.execute("select count(*) as count from ums_menu where menu_pid=%s", (menu_id,))
            child_count = cursor.fetchone()["count"]
            if child_count > 0:
                return error_response("当前菜单下存在子菜单，无法删除", 400)

            # 删除 ums_role_menu 关联
            cursor.execute("delete from ums_role_menu where menu_id=%s", (menu_id,))

            cursor.execute("delete from ums_menu where menu_id=%s", (menu_id,))
            conn.commit()
        return success_response("菜单删除成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 启用/禁用菜单
def update_menu_status(menu_id, hidden):
    if not menu_exist(menu_id):
        return error_response("菜单不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("update ums_menu set hidden=%s where menu_id=%s", (hidden, menu_id))
            conn.commit()
        return success_response("菜单显示状态已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

#  获取所有菜单，以树形结构返回
def get_menu_tree():

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 获取所有菜单
            cursor.execute("select * from ums_menu order by level asc, menu_id asc")
            menus = cursor.fetchall()

        # 构建树形结构
        menu_dict = {menu["menu_id"]: menu for menu in menus}
        menu_tree = []

        for menu in menus:
            menu["children"] = []
            if menu["menu_pid"]:
                parent = menu_dict.get(menu["menu_pid"])
                if parent:
                    parent["children"].append(menu)
            else:
                menu_tree.append(menu)

        return success_response(menu_tree, "获取树形菜单成功")

    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()


# 获取指定菜单的上下级菜单
def get_menu_hierarchy(menu_id, page, page_size):
    if not menu_exist(menu_id):
        return error_response("菜单不存在", 404)
    offset, limit = paginate_query(page, page_size)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 当前菜单
            cursor.execute("select * from ums_menu where menu_id=%s", (menu_id,))
            menu = cursor.fetchone()

            if not menu:
                return error_response("菜单不存在", 404)

            # 上级菜单
            parent_menu = None
            if menu["menu_pid"]:
                cursor.execute("select * from ums_menu where menu_id=%s", (menu["menu_pid"],))
                parent_menu = cursor.fetchone()

            # 下级菜单
            cursor.execute("select * from ums_menu where menu_pid=%s limit %s offset %s", (menu_id,limit,offset))
            child_menus = cursor.fetchall()
            cursor.execute("select count(*) as total from ums_menu where menu_pid=%s", (menu_id,))
            total_child_menus = cursor.fetchone()["total"]

        return success_response({
            "current_menu": menu,
            "parent_menu": parent_menu,
            "child_menus": child_menus,
            "child_total": total_child_menus,
            "page": page,
            "page_size": page_size
        }, "获取菜单层级成功")

    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()



