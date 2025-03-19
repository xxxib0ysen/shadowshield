import hashlib
import re
import pymysql
import requests

# from app.utils.adblock_parser import get_rules_from_redis, fetch_adblock_rules
from app.utils.common import paginate_query
from connect import create_connection
from app.utils.response import *
from datetime import datetime


# 广告屏蔽源管理
class SourceService:
    # 计算规则文件的 SHA256 哈希值
    @staticmethod
    def calculate_checksum(content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    # 解析输入的规则源（格式：规则名称 | 规则URL，支持换行符、*、>）
    @staticmethod
    def parse_source(input_text):
        sources = []
        for line in input_text.splitlines():
            clean_line = line.strip()
            if "|" not in clean_line:
                continue  # 必须包含 "规则名称|规则URL"

            source_name, source_url = map(str.strip, clean_line.split("|", 1))

            # 处理通配符 * 和 >
            source_url = source_url.replace("*", "").replace(">", "")

            # 仅存储有效的 http(s) URL
            if source_name and re.match(r'^https?://', source_url):
                sources.append((source_name, source_url))

        return sources

    # 导入广告屏蔽源（批量）
    @staticmethod
    def add(input_text):
        sources = SourceService.parse_source(input_text)
        if not sources:
            return error_response("请输入有效的广告屏蔽源，格式：规则名称 | 规则URL", 400)

        success_count, fail_count = 0, 0

        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                sql = """
                insert into adblock_source (source_name, source_url, createdon)
                values (%s, %s, now())
                """

                for source_name, source_url in sources:
                    try:
                        cursor.execute(sql, (source_name, source_url))
                        success_count += 1
                        # **解析规则并存入 Redis**
                        fetch_adblock_rules(source_url)
                    except pymysql.MySQLError:
                        fail_count += 1

            conn.commit()
            return success_response({"success_count": success_count, "fail_count": fail_count})
        except pymysql.MySQLError as e:
            return error_response(f"数据库错误: {str(e)}", 500)

    # 分页获取（按最后更新时间排序）
    @staticmethod
    def getList(page,page_size):
        try:
            conn = create_connection()
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 获取总记录数
                sql_count = "select count(*) as total from adblock_source"
                cursor.execute(sql_count)
                total_count = cursor.fetchone()["total"]

                offset, page_size = paginate_query(page, page_size)

                sql = """
                        select * from adblock_source 
                        order by last_modified desc
                        limit %s offset %s
                        """
                cursor.execute(sql, (page_size, offset))
                sources = cursor.fetchall()

                # **从 Redis 获取解析后的规则**
                for source in sources:
                    source["parsed_rules"] = get_rules_from_redis(source["source_url"])


                return success_response({
                    "total": total_count,
                    "page": page,
                    "page_size": page_size,
                    "data": sources
                })
        except pymysql.MySQLError as e:
            return error_response(f"数据库查询失败: {str(e)}", 500)

    # 删除广告屏蔽源
    @staticmethod
    def delete(source_id):
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                sql = "delete from adblock_source where source_id = %s"
                cursor.execute(sql, (source_id,))
            conn.commit()
            return success_response("规则源删除成功")
        except pymysql.MySQLError as e:
            return error_response(f"删除失败: {str(e)}", 500)

    # 启用/禁用广告屏蔽源
    @staticmethod
    def update_status(source_id, status):
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                sql = "update adblock_source set status = %s where source_id = %s"
                cursor.execute(sql, (status, source_id))
            conn.commit()
            return success_response("状态更新成功")
        except pymysql.MySQLError as e:
            return error_response(f"状态更新失败: {str(e)}", 500)

    # 同步官方规则源更新（基于 Last-Modified、ETag、Checksum）
    @staticmethod
    def update_sources():
        updated_count, skipped_count, failed_count = 0, 0, 0

        try:
            conn = create_connection()
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "select source_id, source_url, last_modified, etag, checksum from adblock_source where status = 1"
                cursor.execute(sql)
                sources = cursor.fetchall()

                for source in sources:
                    source_id = source['source_id']
                    source_url = source['source_url']
                    last_modified_db = source.get('last_modified')
                    etag_db = source.get('etag')
                    checksum_db = source.get('checksum')

                    try:
                        headers = {'User-Agent': 'Mozilla/5.0'}
                        response = requests.head(source_url, timeout=10, headers=headers)

                        if response.status_code != 200:
                            failed_count += 1
                            continue

                        etag_web = response.headers.get('ETag')
                        last_modified_web = response.headers.get('Last-Modified')

                        # ETag 校验
                        if etag_db and etag_web and etag_db == etag_web:
                            skipped_count += 1
                            continue

                        # Last-Modified 校验
                        if last_modified_db and last_modified_web and last_modified_db == last_modified_web:
                            skipped_count += 1
                            continue

                        # 下载最新规则文件
                        response = requests.get(source_url, timeout=10, headers=headers)
                        if response.status_code != 200:
                            failed_count += 1
                            continue

                        rule_content = response.text
                        new_checksum = SourceService.calculate_checksum(rule_content)

                        # Checksum 校验
                        if checksum_db and new_checksum == checksum_db:
                            skipped_count += 1
                            continue

                        # 更新数据库
                        sql_update = """
                            update adblock_source 
                            set last_modified = %s, etag = %s, checksum = %s 
                            where source_id = %s
                        """
                        cursor.execute(sql_update, (last_modified_web, etag_web, new_checksum, source_id))
                        conn.commit()
                        updated_count += 1

                    except requests.RequestException:
                        failed_count += 1
                        continue

            return success_response({
                "updated_count": updated_count,
                "skipped_count": skipped_count,
                "failed_count": failed_count
            })
        except pymysql.MySQLError as e:
            return error_response(f"更新失败: {str(e)}", 500)
