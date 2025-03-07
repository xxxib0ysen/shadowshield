import pymysql
from app.utils.common import paginate_query, resource_category_exist
from app.utils.response import success_response, error_response
from connect import create_connection

# 分页查询
def list_resource_category(page, page_size):
    offset, limit = paginate_query(page, page_size)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select * from ums_resource_category order by createdon desc limit %s offset %s", (limit, offset))
            categories = cursor.fetchall()
            cursor.execute("select count(*) as total from ums_resource_category")
            total = cursor.fetchone()["total"]

        return success_response({"categories": categories, "total": total, "page": page, "page_size": page_size}, "获取资源分类成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()

# 添加
def create_resource_category(data):
    category_name = data.get("category_name")
    if not category_name:
        return error_response("资源分类名称不能为空", 400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 检查资源分类是否已存在
            cursor.execute("select category_id from ums_resource_category where category_name=%s", (category_name,))
            if cursor.fetchone():
                return error_response("资源分类已存在", 400)

            sql = "insert into ums_resource_category (category_name, createdon) values (%s, now())"
            cursor.execute(sql, (category_name,))
            conn.commit()
        return success_response("资源分类创建成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 修改资源分类
def update_resource_category(category_id, data):
    if not resource_category_exist(category_id):
        return error_response("资源分类不存在", 404)

    category_name = data.get("category_name")
    if not category_name:
        return error_response("资源分类名称不能为空", 400)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 检查名称是否存在
            cursor.execute("select category_id from ums_resource_category where category_name=%s and category_id!=%s",
                           (category_name, category_id))
            if cursor.fetchone():
                return error_response("资源分类名称已存在", 400)
            cursor.execute("update ums_resource_category set category_name=%s where category_id=%s", (category_name, category_id))
            conn.commit()
        return success_response("资源分类更新成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 删除资源分类
def delete_resource_category(category_id):
    if not resource_category_exist(category_id):
        return error_response("资源分类不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 检查是否有资源属于该分类
            cursor.execute("select count(*) as count from ums_resource where category_id=%s", (category_id,))
            resource_count = cursor.fetchone()["count"]

            if resource_count > 0:
                return error_response("该资源分类下存在资源，无法删除", 400)

            cursor.execute("delete from ums_resource_category where category_id=%s", (category_id,))
            conn.commit()
        return success_response("资源分类已删除")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()
