import requests
from bs4 import BeautifulSoup
import re

# 网页地址
url = "https://www.wetest.vip/page/cloudflare/address_v4.html"

# 发送请求并获取网页内容
response = requests.get(url)

# 确保请求成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有有效 IP 地址所在的表格
    rows = soup.select('table.layui-table tbody tr')

    # 创建一个空的列表来存储 IP 地址
    ip_addresses = []

    # 正则表达式，用于检查 IP 地址
    ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')

    # 过滤掉广告信息并提取每一行中的 IP 地址
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 1:
            ip_address = columns[1].text.strip()

            # 使用正则表达式验证该字符串是否为有效的 IP 地址
            if ip_pattern.match(ip_address):
                # 检查是否包含广告链接，过滤掉包含广告的行
                ad_links = row.find_all('a')
                if not ad_links:  # 如果该行没有广告链接，则添加 IP 地址
                    ip_addresses.append(ip_address)

    # 将 IP 地址写入文本文件
    with open("ip.txt", "w") as file:
        for ip in ip_addresses:
            file.write(ip + '\n')

    print(f"成功提取 {len(ip_addresses)} 个 IP 地址，并保存到 cf_ips.txt 文件中。")
else:
    print("无法访问网页，状态码：", response.status_code)
