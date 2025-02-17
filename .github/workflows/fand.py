import os
import requests
import re

def escape_markdown_v2(text):
    """转义 Telegram MarkdownV2 特殊字符"""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

def send_telegram_message(content):
    """发送 Telegram 消息，支持 MarkdownV2 格式"""
    escaped_content = escape_markdown_v2(content)
    content_with_line_breaks = escaped_content.replace("\n", "  \n")  # MarkdownV2 换行
    spoiler_content = f'||{content_with_line_breaks}||'  # 添加剧透效果
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': spoiler_content,
        'parse_mode': 'MarkdownV2'
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"发送消息到 Telegram 时发生错误: {response.text}")

# 获取 GitHub Secrets
api_token = os.environ.get("CLOUDFLARE_API_TOKEN")
zone_id = os.environ.get("CF_ZONE_ID")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
name = "fand"
ipdb_api_url = "https://raw.githubusercontent.com/ymyuuu/IPDB/refs/heads/main/bestproxy.txt"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
}

def delete_dns_record(record_id):
    try:
        delete_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        response = requests.delete(delete_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to delete DNS record with ID {record_id}: {response.text}")
       # send_telegram_message(f"成功删除 DNS 记录: {record_id}")
    except Exception as e:
        print(f"Exception occurred while deleting DNS record with ID {record_id}: {str(e)}")


def create_dns_record(ip):
    try:
        create_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        create_data = {
            "type": "A",
            "name": name,
            "content": ip,
            "ttl": 60,
            "proxied": False,
        }
        response = requests.post(create_url, headers=headers, json=create_data)
        if response.status_code != 200:
            raise Exception(f"Failed to create DNS record for IP {ip}: {response.text}")
        send_telegram_message(f"成功创建 DNS 记录: {name} ip:{ip}")
    except Exception as e:
        print(f"Exception occurred while creating DNS record for IP {ip}: {str(e)}")

try:
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    response = requests.get(url, headers=headers)
    data = response.json()

    for record in data.get("result", []):
        record_name = record.get("name", "")
        if re.search(name, record_name):
            delete_dns_record(record["id"])
    
    print(f"Successfully deleted records with name {name}, updating DNS records now")
  #  send_telegram_message(f"成功删除 {name} 旧的 DNS 记录，准备更新新的 IP 地址")

    ipdb_response = requests.get(ipdb_api_url)
    new_ip_list = ipdb_response.text.strip().split("\n")

    if new_ip_list:
        first_ip = new_ip_list[0]
        create_dns_record(first_ip)
        print(f"Successfully updated {name} DNS records")
except Exception as e:
    print(f"Exception occurred: {str(e)}")
