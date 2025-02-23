import csv
import requests
from requests_html import HTMLSession
from colorama import Fore, Style

# 创建HTMLSession对象
session = HTMLSession()

# 设置目标URL
url = 'https://www.proxydocker.com/en/proxylist/country/Taiwan'

# 请求头
headers = {'User-Agent': 'Mozilla/5.0'}

# 初始化IP列表
ip_list = []

# 开始获取IP地址
try:
    # 发起请求
    r = session.get(url, headers=headers)
    print(f"Status Code: {r.status_code}")
    
    # 渲染网页，确保动态内容加载完毕
    r.html.render(sleep=2, keep_page=True, scrolldown=1)

    # 获取IP和端口
    for i in range(1, 51):  # 假设最多获取50个IP
        ip = r.html.xpath(f'//*[@id="proxylist_table"]/tr[{i}]/td[1]', first=True).text
      #  port = r.html.xpath(f'//*[@id="proxylist_table"]/tr[{i}]/td[2]', first=True).text
        
        if ip:
            # 如果端口是SOCKS类型的代理，则跳过
            if 'SOCK' not in port:
                # 拼接IP和端口，添加到列表
                ip_list.append(f"{port.lower()}://{ip}")
    
    print(Fore.GREEN + "IP addresses successfully retrieved!" + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)

with open('ip.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["IP Address"])  # 写入表头
    for ip in ip_list:
        writer.writerow([ip])  # 写

print(Fore.YELLOW + "Valid IP list has been completed." + Style.RESET_ALL)
