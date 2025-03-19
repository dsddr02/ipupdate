import requests
import re

EASYLIST_URL = "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_adservers.txt"
OUTPUT_FILE = "adblock.list"

def download_easylist(url):
    """下载 EasyList 广告域名列表"""
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def is_valid_domain(domain):
    """检查是否为合法域名（避免 Mihomo 解析错误）"""
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", domain):  # 过滤 IP
        return False
    if domain.endswith(".") or not re.search(r"[a-zA-Z]", domain):  # 过滤无效域名
        return False
    return True

def parse_easylist(lines):
    """解析 EasyList 并提取域名"""
    domains = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("!") or "/" in line or "*" in line:
            continue
        if line.startswith("||"):
            domain = line[2:].split("^")[0]
        elif line.startswith("."):
            domain = line[1:]
        elif "." in line:
            domain = line
        else:
            continue

        if is_valid_domain(domain):
            domains.add(domain)
    
    return domains

def save_to_list(domains, filename):
    """保存为 .list 文件"""
    with open(filename, "w", encoding="utf-8") as file:
        for domain in sorted(domains):
           # file.write(f"+.{domain}\n")
            file.write(f"domain:{domain}\n")
    print(f"✅ 已保存 {len(domains)} 个广告域名到 {filename}")

def main():
    lines = download_easylist(EASYLIST_URL)
    domains = parse_easylist(lines)
    save_to_list(domains, OUTPUT_FILE)

if __name__ == "__main__":
    main()
