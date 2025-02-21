import requests
import re

# 获取网页内容
url = "https://raw.githubusercontent.com/ZhiXuanWang/cf-speed-dns/refs/heads/main/index.html"
response = requests.get(url)
response.raise_for_status()  # 确保请求成功

# 正则匹配 IPv4 地址
ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
ips = ip_pattern.findall(response.text)

# 去重并排序
ips = sorted(set(ips))

# 保存到 txt 文件
with open("ips.txt", "w") as f:
    f.write("\n".join(ips))

print(f"共提取 {len(ips)} 个 IP 地址，并已保存到 ips.txt 文件。")
