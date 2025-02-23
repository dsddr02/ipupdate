from bs4 import BeautifulSoup
import requests
import csv
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
                port = cols[1].text.strip() if cols[1] else None
                if ip and port:
                    ip_list.append(f"{port.lower()}://{ip}")
    
    else:
        print(Fore.RED + "Failed to fetch page!" + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)

# 验证获取的IP是否有效
valid_ip_list = []
for ip in ip_list:
    try:
        # 测试IP是否有效，尝试访问一个网页
        res = requests.get('https://www.youtube.com/?hl=zh-TW&gl=TW', proxies={'http': ip, 'https': ip}, timeout=5)
        if res.status_code == 200:
            valid_ip_list.append(ip)
            print(Fore.GREEN + 'SUCCESS: ' + ip + Style.RESET_ALL)
    except requests.RequestException:
        print(Fore.RED + 'FAIL: ' + ip + Style.RESET_ALL)

# 将有效IP写入CSV文件
with open('ip.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Proxy"])
    for ip in valid_ip_list:
        writer.writerow([ip])

print(Fore.YELLOW + "Valid IP list has been completed." + Style.RESET_ALL)
