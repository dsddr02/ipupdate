import requests
import re

# 目标URL
url = "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_adservers.txt"

# 本地文件名（使用 .list 扩展名）
filename = "easylist_adservers.list"

try:
    # 下载文件内容
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # 确保请求成功
    
    # 获取原始文本内容
    original_lines = response.text.splitlines()  # 按行分割文本

    # 过滤掉以 "!" 或 "/" 开头的行，并进行替换
    modified_lines = [
        re.sub(r"\|\|([a-zA-Z0-9.-]+)\^", r"DOMAIN-SUFFIX,\1", line)
        for line in original_lines
        if not line.startswith("!") and not line.startswith("/")
    ]

    # 重新拼接文本
    modified_text = "\n".join(modified_lines)

    # 将修改后的内容保存到 .list 文件
    with open(filename, "w", encoding="utf-8") as file:
        file.write(modified_text)

    print(f"文件已成功下载并处理，保存为 {filename}")

except requests.RequestException as e:
    print(f"下载文件失败: {e}")
except Exception as e:
    print(f"处理文件时出错: {e}")
