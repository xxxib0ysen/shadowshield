import json
import requests
import redis
import re

# 连接 Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# 解析域名拦截规则
def extract_domain_rules(rule_list):
    domain_rules = []

    # 只匹配 ||domain.com^ 这样的规则
    domain_pattern = re.compile(r'^\|\|([a-zA-Z0-9.-]+)\^')

    for rule in rule_list:
        rule = rule.strip()

        # 跳过非域名规则
        if rule.startswith("!") or rule.startswith("#") or rule.startswith("@@") or "##" in rule or "#?#" in rule:
            continue

        # 匹配域名规则
        match = domain_pattern.match(rule)
        if match:
            domain_rules.append(match.group(1))  # 提取 domain.com 部分

    return domain_rules


# 下载广告规则，并存入 Redis
def fetch_adblock_rules(source_url):
    try:
        response = requests.get(source_url, timeout=10)
        if response.status_code != 200:
            return None

        # 按行拆分规则，并去除注释
        rule_lines = response.text.split("\n")
        raw_rules = [line.strip() for line in rule_lines if line.strip() and not line.startswith("!")]

        # 过滤掉非法的 `\x` 转义字符
        raw_rules = [re.sub(r'\\x[0-9A-Fa-f]{2}', '', r) for r in raw_rules]

        # 提取域名拦截规则
        domain_rules = extract_domain_rules(raw_rules)

        # 存储到 Redis
        redis_client.set(source_url, json.dumps(domain_rules))

        return domain_rules
    except requests.RequestException:
        return None


# 从 Redis 获取存储的域名
def get_rules_from_redis(source_url):
    rules = redis_client.get(source_url)
    return json.loads(rules) if rules else []



# 测试
# source_url = "https://filters.adtidy.org/android/filters/2_optimized.txt"  # 替换成真实的规则链接
# fetch_adblock_rules(source_url)
# domains = get_rules_from_redis(source_url)
# print(domains)
