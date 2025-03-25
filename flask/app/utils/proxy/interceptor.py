import re
from app.services.control.CustomService import get_enabled_custom_rules
from app.services.rule.WebsiteService import get_enabled_type_url_map, get_enabled_type_ids
from app.services.system.SettingService import is_website_blocking_enabled


# 通配符匹配函数：支持 *, >
def match_rules(target_url, rule_list):
    for rule in rule_list:
        if rule == target_url:
            return True
        if "*" in rule or ">" in rule:
            try:
                pattern = rule.replace(".", r"\.").replace("*", ".*").replace(">", ".+")
                if re.fullmatch(pattern, target_url):
                    return True
            except:
                continue
    return False

# 判断某 URL 是否应拦截
def should_block_url(target_url):
    # 控制开关
    if not is_website_blocking_enabled():
        return False

    # 优先级 1：自定义规则
    custom_rules = get_enabled_custom_rules()
    if match_rules(target_url, custom_rules):
        return True

    # 优先级 2：类型规则，需要类型启用 + 网址启用
    type_ids = get_enabled_type_ids()
    type_url_map = get_enabled_type_url_map()

    for tid in type_ids:
        urls = type_url_map.get(tid, [])
        if match_rules(target_url, urls):
            return True

    return False

