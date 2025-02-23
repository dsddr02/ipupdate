import csv
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

# 设置目标URL
url = 'https://www.proxydocker.com/en/proxylist/country/Taiwan'

# 请求头
headers = {'User-Agent': 'Mozilla/5.0'}

# 初始化IP列表
ip_list = []

# 发起请求获取页面内容
try:
    r = requests.get(url, headers=headers)
    print(f"Status Code: {r.status_code}")
    
    if r.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 找到表格的行数据
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].text.strip() if cols[0] else None
                if ip:  # 只保存IP地址
                    ip_list.append(ip)  # 添加IP地址到列表
    
    else:
        print(Fore.RED + "Failed to fetch page!" + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)

# 将IP列表直接保存到CSV文件
with open('ip.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["IP Address"])  # 写入表头
    for ip in ip_list:
        writer.writerow([ip])  # 写入每一行IP

print(Fore.YELLOW + "IP list has been saved to 'ip_list.csv'." + Style.RESET_ALL)
