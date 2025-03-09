import pymysql
from app.utils.common import paginate_query, resource_exist, resource_category_exist, format_datetime
from app.utils.response import success_response, error_response
from connect import create_connection


# 分页/按分类、名称、uri
def list_resource(category_id, name_keyword, uri_keyword, page, page_size):
    offset, limit = paginate_query(page, page_size)

    filters = []
    values = []

    if category_id:
        filters.append("category_id = %s")
        values.append(category_id)

    if name_keyword:
        filters.append("name LIKE %s")
        values.append(f"%{name_keyword}%")

    if uri_keyword:
        filters.append("uri LIKE %s")
        values.append(f"%{uri_keyword}%")

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 获取分页数据
            sql = f"""
                select * from ums_resource 
                {where_clause}
                limit %s offset %s
            """
            cursor.execute(sql, (*values, limit, offset))
            resources = cursor.fetchall()

            count_sql = f"select count(*) as total from ums_resource {where_clause}"
            cursor.execute(count_sql, tuple(values))
            total = cursor.fetchone()["total"]

            for resource in resources:
                resource["createdon"] = format_datetime(resource["createdon"])

        return success_response({
            "resources": resources,
            "total": total,
            "page": page,
            "page_size": page_size
        })
    except pymysql.MySQLError as e:
        return error_response(f"数据库查询失败: {str(e)}", 500)
    finally:
        conn.close()


# 添加
def create_resource(data):
    name = data.get("name")
    uri = data.get("uri")
    category_id = data.get("category_id")
    description = data.get("description", "")

    if not name or not category_id:
        return error_response("资源名称和分类 ID 不能为空", 400)

    if not resource_category_exist(category_id):
        return error_response("资源分类不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 检查 name 和 uri 是否唯一
            cursor.execute("select resource_id from ums_resource where name=%s or uri=%s", (name, uri))
            if cursor.fetchone():
                return error_response("资源名称或 URI 已存在", 400)

            sql = """
                insert into ums_resource (name, category_id, uri, description, createdon) 
                values (%s, %s, %s, %s, NOW())
            """
            cursor.execute(sql, (name, category_id, uri, description))
            conn.commit()
        return success_response("资源创建成功")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 修改
def update_resource(resource_id, data):
    if not resource_exist(resource_id):
        return error_response("资源不存在", 404)

    name = data.get("name")
    uri = data.get("uri")
    category_id = data.get("category_id")
    description = data.get("description")

    if category_id and not resource_category_exist(category_id):
        return error_response("资源分类不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            update_fields = []
            update_values = []

            if name or uri:
                cursor.execute("select resource_id from ums_resource where (name=%s or uri=%s) and resource_id!=%s",
                               (name, uri, resource_id))
                if cursor.fetchone():
                    return error_response("资源名称或 URI 已存在", 400)

            if name:
                update_fields.append("name=%s")
                update_values.append(name)

            if uri:
                update_fields.append("uri=%s")
                update_values.append(uri)

            if category_id:
                update_fields.append("category_id=%s")
                update_values.append(category_id)

            if description is not None:
                update_fields.append("description=%s")
                update_values.append(description)

            if not update_fields:
                return error_response("没有需要更新的字段", 400)

            sql = f"update ums_resource set {', '.join(update_fields)} where resource_id=%s"
            update_values.append(resource_id)
            cursor.execute(sql, tuple(update_values))
            conn.commit()

        return success_response("资源信息已更新")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

# 删除
def remove_resource(resource_id):
    if not resource_exist(resource_id):
        return error_response("资源不存在", 404)

    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 删除 ums_role_resource 中的关联数据
            cursor.execute("delete from ums_role_resource where resource_id=%s", (resource_id,))
            # 删除 ums_resource
            cursor.execute("delete from  ums_resource where resource_id=%s", (resource_id,))
            conn.commit()
        return success_response("资源及其关联数据已删除")
    except pymysql.MySQLError as e:
        return error_response(f"数据库操作失败: {str(e)}", 500)
    finally:
        conn.close()

