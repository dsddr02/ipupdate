import requests
from bs4 import BeautifulSoup

# 获取网页内容
url = "https://ipdb.030101.xyz/bestcf/"
response = requests.get(url)

# 检查网页是否成功获取
if response.status_code == 200:
    # 解析网页
    soup = BeautifulSoup(response.text, "html.parser")

    # 查找表格
    table = soup.find("table", {"id": "csvTable"})
    if table:
        # 查找所有表格行
        rows = table.find_all("tr")

        # 存储 IP 地址
        ip_addresses = []

        # 遍历表格行，提取 IP 地址（假设 IP 地址在第二列）
        for row in rows[1:]:  # 跳过表头
            cols = row.find_all("td")
            if len(cols) > 1:
                ip = cols[1].text.strip()  # 假设 IP 地址在第二列
                ip_addresses.append(ip)

        # 保存 IP 地址到文件
        with open("ip_addresses.txt", "w") as f:
            for ip in ip_addresses:
                f.write(ip + "\n")

        print("IP 地址已保存到 ip_addresses.txt")
    else:
        print("未找到表格")
else:
    print("网页获取失败，状态码:", response.status_code)
