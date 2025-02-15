import requests
import traceback
import time
import os
import json
import re
import requests
# API 密钥
CF_API_TOKEN    =   os.environ["CF_API_TOKEN"]
CF_ZONE_ID      =   os.environ["CF_ZONE_ID"]
CF_DNS_NAME     =   os.environ["CF_DNS_NAME"]

# Telegram bot token and chat ID
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

headers = {
    'Authorization': f'Bearer {CF_API_TOKEN}',
    'Content-Type': 'application/json'
}

def get_cf_speed_test_ip(timeout=10, max_retries=5):
    for attempt in range(max_retries):
        try:
            # 发送 GET 请求，设置超时
            response = requests.get('https://ip.164746.xyz/ipTop.html', timeout=timeout)
            # 检查响应状态码
            if response.status_code == 200:
                return response.text
        except Exception as e:
            traceback.print_exc()
            print(f"get_cf_speed_test_ip Request failed (attempt {attempt + 1}/{max_retries}): {e}")
    # 如果所有尝试都失败，返回 None 或者抛出异常，根据需要进行处理
    return None

# 获取 DNS 记录
def get_dns_records(name):
    def_info = []
    url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json()['result']
        for record in records:
            if record['name'] == name:
                def_info.append(record['id'])
        return def_info
    else:
        print('Error fetching DNS records:', response.text)

# 更新 DNS 记录
def update_dns_record(record_id, name, cf_ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{record_id}'
    data = {
        'type': 'A',
        'name': name,
        'content': cf_ip,
        'ttl': 60
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"cf_dns_change success: ---- Time: " + str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " ---- ip：" + str(cf_ip))
        return "ip:" + str(cf_ip) + "解析" + str(name) + "成功"
    else:
        traceback.print_exc()
        print(f"cf_dns_change ERROR: ---- Time: " + str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return "ip:" + str(cf_ip) + "解析" + str(name) + "失败"

# Telegram message push
def escape_markdown_v2(text):
    # 转义 Markdown v2 特殊字符（包括点号 .）
    escape_chars = r"\\\*_{}[]()#+-.!`"  # 加入点号 . 

    # 使用正则表达式，将所有特殊字符前加上反斜杠
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)

def send_telegram_message(content):
    # 转义特殊字符
    escaped_content = escape_markdown_v2(content)

    # 替换文本中的换行符为 Markdown v2 支持的换行方式
    content_with_line_breaks = escaped_content.replace("\n", "  \n")  # 用 "  \n" 实现换行

    # 添加剧透效果
    spoiler_content = "||" + content_with_line_breaks + "||"

    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': spoiler_content,
        'parse_mode': 'MarkdownV2'  # 使用 MarkdownV2
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code != 200:
        print(f"发送消息到 Telegram 时发生错误: {response.text}")

# 主函数
def main():
    # 获取最新优选IP
    ip_addresses_str = get_cf_speed_test_ip()
    ip_addresses = ip_addresses_str.split(',')
    dns_records = get_dns_records(CF_DNS_NAME)
    push_telegram_content = []
    # 遍历 IP 地址列表
    for index, ip_address in enumerate(ip_addresses):
        # 执行 DNS 变更
        dns = update_dns_record(dns_records[index], CF_DNS_NAME, ip_address)
        push_telegram_content.append(dns)

    send_telegram_message('\n'.join(push_telegram_content))

if __name__ == '__main__':
    main()
