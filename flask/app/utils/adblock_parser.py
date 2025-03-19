import json
import requests
import redis
from adblockparser import AdblockRules

# 连接 Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# 下载广告规则，并使用 adblockparser 解析，存入 Redis
def fetch_adblock_rules(source_url):
    try:
        response = requests.get(source_url, timeout=10)
        if response.status_code != 200:
            return None

        # 按行拆分规则
        rule_lines = response.text.split("\n")
        raw_rules = [line.strip() for line in rule_lines if line.strip() and not line.startswith("!")]

        # 用 AdblockRules 解析规则
        rule_parser = AdblockRules(raw_rules)

        # 获取 adblockparser 能识别的规则
        parsed_rules = [rule for rule in raw_rules if rule_parser.should_block(rule)]

        # 存储解析后的规则到 Redis
        redis_client.set(source_url, json.dumps(parsed_rules))

        return parsed_rules
    except requests.RequestException:
        return None

# 从 Redis 获取存储的广告规则
def get_rules_from_redis(source_url):
    rules = redis_client.get(source_url)
    return json.loads(rules) if rules else []
