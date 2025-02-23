import requests
from requests_html import HTMLSession
from colorama import Fore, Style

# 创建HTMLSession对象
session = HTMLSession()

# 设置目标URL
url = 'https://www.proxydocker.com/en/proxylist/port/443'

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

    # 获取IP地址，最多获取50个IP
    for i in range(1, 51):
        ip = r.html.xpath(f'//*[@id="proxylist_table"]/tr[{i}]/td[1]', first=True).text
        
        if ip:
            # 去掉端口，只保留IP地址
            ip_address = ip.split(":")[0]  # 仅提取IP，去掉端口
            ip_list.append(ip_address)
    
    print(Fore.GREEN + "IP addresses successfully retrieved!" + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)

# 保存IP到txt文件
with open('ip_py.txt', 'w') as txtfile:
    for ip in ip_list:
        txtfile.write(f"{ip}\n")  # 每个IP写入新的一行

print(Fore.YELLOW + "IP list has been saved to 'ip_list.txt'." + Style.RESET_ALL)
