import requests

# EasyList 广告服务器列表 URL
EASYLIST_URL = "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_adservers.txt"

# 目标文件路径
OUTPUT_FILE = "adblock.list"

def download_easylist(url):
    """ 下载 EasyList 广告服务器列表 """
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def parse_easylist(lines):
    """ 解析 EasyList 规则，提取有效域名 """
    domains = set()
    for line in lines:
        line = line.strip()
        # 忽略注释、空行和非域名规则
        if not line or line.startswith("!") or "/" in line or "*" in line:
            continue
        # 去除前缀，比如 ||example.com^
        if line.startswith("||"):
            domain = line[2:].split("^")[0]  # 仅保留主域名
            domains.add(domain)
        elif line.startswith("."):
            domains.add(line[1:])  # 移除前导 .
        elif "." in line:
            domains.add(line)
    return domains

def save_to_list(domains, filename):
    """ 生成 Clash 兼容的 `.list` 文件 """
    with open(filename, "w", encoding="utf-8") as file:
        file.write("payload:\n")
        for domain in sorted(domains):
            file.write(f"  - '+.{domain}'\n")
    print(f"已保存 {len(domains)} 个广告域名到 {filename}")

def main():
    print("正在下载 EasyList 广告服务器列表...")
    lines = download_easylist(EASYLIST_URL)
    print(f"下载完成，共 {len(lines)} 行")

    print("正在解析规则...")
    domains = parse_easylist(lines)
    print(f"解析完成，共提取 {len(domains)} 个广告域名")

    print("正在保存到 .list 文件...")
    save_to_list(domains, OUTPUT_FILE)

if __name__ == "__main__":
    main()
