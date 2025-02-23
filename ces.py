import csv
import requests
import HTMLSession
import Fore, Style

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
        port = r.html.xpath(f'//*[@id="proxylist_table"]/tr[{i}]/td[2]', first=True).text
        
        if ip and port:
            # 如果端口是SOCKS类型的代理，则跳过
            if 'SOCK' not in port:
                # 拼接IP和端口，添加到列表
                ip_list.append(f"{port.lower()}://{ip}")
    
    print(Fore.GREEN + "IP addresses successfully retrieved!" + Style.RESET_ALL)

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
with open('valid_ip.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Proxy"])
    for ip in valid_ip_list:
        writer.writerow([ip])

print(Fore.YELLOW + "Valid IP list has been completed." + Style.RESET_ALL)
