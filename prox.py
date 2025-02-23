from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import requests
import re

# 设置 Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 无头模式（不显示浏览器窗口）
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")

# 初始化浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 打开网页
url = "https://ipdb.030101.xyz/bestproxy/"
driver.get(url)

# 等待页面加载（调整等待时间以确保页面内容加载完全）
time.sleep(5)  # 等待5秒，确保数据加载完成

# 获取表格
table = driver.find_element(By.ID, "csvTable")
# 提取表格中的 IP 地址（假设 IP 地址在第一列，第三列为数值列）
rows = table.find_elements(By.TAG_NAME, "tr")

# Telegram 设置
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
name = "yx1"
ipdb_api_url = "https://raw.githubusercontent.com/ymyuuu/IPDB/refs/heads/main/bestcf.txt"
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

# 遍历表格行并查找符合条件的 IP 地址
for row in rows[1:]:  # 跳过表头
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) > 2:  # 确保该行有数据
        ip = cols[0].text.strip()  # IP 地址在第一列
        third_column_value = cols[3].text.strip()  # 获取第三列数值
        # 如果第三列的值为 0.00，跳过此行
        if third_column_value == "0.00":
            print(f"第三列值为 0.00，跳过 IP 地址 {ip}")
            driver.quit()
            break
        # 如果第三列的值大于 0.00，获取第一行 IP 并更新 DNS 记录
        if third_column_value > "0.00":
            first_ip = ip
            try:
                # 删除旧的 DNS 记录
                url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
                response = requests.get(url, headers=headers)
                data = response.json()
                for record in data.get("result", []):
                    record_name = record.get("name", "")
                    if re.search(name, record_name):
                        delete_dns_record(record["id"])
                # 创建新的 DNS 记录
                create_dns_record(first_ip)
                print(f"成功更新 {name} 的 DNS 记录为 IP: {first_ip}")
                send_telegram_message(f"成功更新 {name} 的 DNS 记录为 IP: {first_ip}")
            except Exception as e:
                print(f"Exception occurred during DNS record update: {str(e)}")
            driver.quit()
            break
else:
    # 如果没有找到符合条件的行
    print("没有找到符合条件的 IP 地址。程序结束。")
    driver.quit()
