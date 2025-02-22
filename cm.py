from bs4 import BeautifulSoup
import requests

# 获取网页内容
url = "https://cf.090227.xyz/"
response = requests.get(url)

# 确保网页请求成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 假设数据在某个表格中，提取表格行
    valid_ips = []
    for row in soup.find_all('tr'):  # 查找所有表格行
        cells = row.find_all('td')
        if len(cells) >= 2:  # 确保有至少两列数据（IP和速度）
            ip = cells[0].text.strip()
            speed = cells[1].text.strip()
            if speed != '0':  # 筛选速度不为0的IP
                valid_ips.append(ip)

    # 将有效的IP地址写入txt文件
    with open("valid_ips.txt", "w") as file:
        for ip in valid_ips:
            file.write(f"{ip}\n")
    
    print(f"成功写入{len(valid_ips)}个IP地址到valid_ips.txt")
else:
    print(f"请求失败，状态码: {response.status_code}")
