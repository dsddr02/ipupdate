import requests
from bs4 import BeautifulSoup

# 网页地址
url = "https://www.wetest.vip/page/cloudflare/address_v4.html"

# 发送请求并获取网页内容
response = requests.get(url)

# 确保请求成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有 IP 地址所在的表格行
    rows = soup.select('table.layui-table tbody tr')

    # 创建一个空的列表来存储 IP 地址
    ip_addresses = []

    # 提取每一行中的 IP 地址
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 1:
            ip_address = columns[1].text.strip()  # 获取第二列，即 IP 地址列
            ip_addresses.append(ip_address)

    # 将 IP 地址写入文本文件
    with open("ip.txt", "w") as file:
        for ip in ip_addresses:
            file.write(ip + '\n')

    print(f"成功提取 {len(ip_addresses)} 个 IP 地址，并保存到 cf_ips.txt 文件中。")
else:
    print("无法访问网页，状态码：", response.status_code)
