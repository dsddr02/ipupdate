from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
url = "https://ipdb.030101.xyz/bestproxy/"
driver.get(url)

# 等待页面加载（调整等待时间以确保页面内容加载完全）
time.sleep(5)  # 等待5秒，确保数据加载完成

# 获取表格
table = driver.find_element(By.ID, "csvTable")

# 提取表格中的 IP 地址（假设 IP 地址在第一列，第三列为数值列）
rows = table.find_elements(By.TAG_NAME, "tr")

# 遍历表格行并查找符合条件的 IP 地址
for row in rows[1:]:  # 跳过表头
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) > 2:  # 确保该行有数据
        ip = cols[0].text.strip()  # IP 地址在第一列
        third_column_value = cols[3].text.strip()  # 获取第三列数值

        # 如果第三列的值为 0.00，写入该 IP 地址并结束程序
        if third_column_value == "0.00":
            with open("prox.txt", "w") as f:
                f.write(ip + "\n")
            print("符合条件的 IP 地址已保存到 prox.txt")
            driver.quit()
            break
else:
    # 如果没有找到符合条件的行
    print("没有找到符合条件的 IP 地址。程序结束。")
    driver.quit()
