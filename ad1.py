import requests

EASYLIST_URL = "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_adservers.txt"
OUTPUT_FILE = "adblock.mrs"

def download_easylist(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def parse_easylist(lines):
    domains = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("!") or "/" in line or "*" in line:
            continue
        if line.startswith("||"):
            domain = line[2:].split("^")[0]
            domains.add(domain)
        elif line.startswith("."):
            domains.add(line[1:])
        elif "." in line:
            domains.add(line)
    return domains

def save_to_mrs(domains, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("payload:\n")
        for domain in sorted(domains):
            file.write(f"  - '+.{domain}'\n")
    print(f"已保存 {len(domains)} 个广告域名到 {filename}")

def main():
    lines = download_easylist(EASYLIST_URL)
    domains = parse_easylist(lines)
    save_to_mrs(domains, OUTPUT_FILE)

if __name__ == "__main__":
    main()
