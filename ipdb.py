from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 设置 Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 无头模式（不显示浏览器窗口）
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")

# 初始化浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 打开网页
url = "https://ipdb.030101.xyz/bestcf/"
driver.get(url)

# 等待页面加载（调整等待时间以确保页面内容加载完全）
time.sleep(5)  # 等待5秒，确保数据加载完成

# 获取表格
table = driver.find_element(By.ID, "csvTable")

# 提取表格中的 IP 地址（假设 IP 地址在第二列）
ip_addresses = []
rows = table.find_elements(By.TAG_NAME, "tr")

# 遍历表格行并提取 IP 地址
for row in rows[1:]:  # 跳过表头
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) > 1:  # 确保该行有数据
        ip = cols[0].text.strip()  # 假设 IP 地址在第二列
        ip_addresses.append(ip)

# 保存 IP 地址到文件
with open("ip_addresses.txt", "w") as f:
    for ip in ip_addresses:
        f.write(ip + "\n")

# 打印提示信息
print("IP 地址已保存到 ip_addresses.txt")

# 关闭浏览器
driver.quit()
