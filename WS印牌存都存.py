from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  # 用於處理 Excel 文件
import os
import time
import requests
from PIL import Image, ImageTk
from math import floor
import re
import tkinter as tk
from tkinter import simpledialog, messagebox

root = tk.Tk()
root.title("WS印牌機器")
root.geometry("600x300")
root.resizable(False, False)
root.attributes("-alpha", 0.0) 

bg_image = Image.open("C:\Users\user\Documents\Card_py\png\logo-ws.png")
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")


canvas.create_text(300, 45, text="請輸入卡片網址", fill="black", font=("微軟正黑體", 16, "bold"))
entry = tk.Entry(root, font=("微軟正黑體", 14), width=30)
canvas.create_window(300, 120, window=entry)

def submit():
    global input_url
    input_url = entry.get()
    if input_url:
        root.destroy()
    else:
        messagebox.showwarning("提醒", "請輸入網址")

btn = tk.Button(root, text="確定", font=("微軟正黑體", 12), command=submit)
canvas.create_window(300, 180, window=btn)

def fade_in(alpha=0.0):
    if alpha < 1.0:
        alpha += 0.05
        root.attributes("-alpha", alpha)
        root.after(30, lambda: fade_in(alpha))


fade_in()

root.mainloop()

speace = []  # 用於存儲空格數量的列表
n=0
# 設定圖片來源資料夾與輸出 PDF 路徑
image_folder = "C:/Users/wei/Documents/YgoCard_png"
output_pdf_path = "C:/Users/wei/Documents/PDF/Ygo_output_cards.pdf"
# 設定 Chrome WebDriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # 如果需要無頭模式，可以取消註解
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
driver = webdriver.Chrome(service=Service("C:/chromedriver-win64/chromedriver.exe"), options=options)
os.makedirs("C:/Users/wei/Documents/YgoCard_png", exist_ok=True)
input_url = "https://ygo.ygosgs.com/#/yugioh"

for file_name in os.listdir(image_folder):
    if file_name.endswith(".jpg"):  # 找到所有 .txt 檔案
        os.remove(os.path.join(image_folder, file_name))
        print(f"{file_name} 已刪除")

# 目標網頁 URL

driver.get(input_url)

delay_time =  30 # 等待時間（秒）


# 用於存儲卡片數據的列表
card_data = []


        
# 定義下載圖片的函數
def download_image(img_url, save_path):
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"圖片已下載：{save_path}")
        else:
            print(f"無法下載圖片，狀態碼：{response.status_code}")
    except Exception as e:
        print(f"下載圖片時發生錯誤：{e}")


try:
    # 等待主元素加載
    main = WebDriverWait(driver, delay_time).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    
    section_main = main.find_element(By.CLASS_NAME, "main-container")
    
    sections = WebDriverWait(section_main, delay_time).until(
        EC.presence_of_element_located((By.XPATH, '//section[contains(@class, "deck-content") and contains(@class, "mt-8")]'))
    )
    # 獲取所有 class 名稱為 "select-none relative max-w-[15rem]" 的元素
    cards = WebDriverWait(sections, delay_time).until(  
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".select-none.relative.max-w-\\[15rem\\]"))
    )

    for card in cards:
        try:
            card_secret_fir = card.find_element(By.CSS_SELECTOR, '.relative.cursor-pointer.group')
            card_secret_sec = card_secret_fir.find_element(By.CSS_SELECTOR, ".w-full.bg-zinc-900.-mt-2.pb-2.pt-4.px-2.rounded-b-xl.flex.flex-col.gap-2")
            ans_secret = card_secret_sec.find_element(By.CSS_SELECTOR, ".flex.items-center.justify-between")
            secret = ans_secret.find_element(By.TAG_NAME, 'span')
            # 將獲得的文本添加到列表中
            card_data.append(secret.text)
        
        except Exception as inner_e:
            print(f"無法處理卡片：{inner_e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 關閉瀏覽器
    driver.quit()
    


#-----卡片數量-----
usingCardData = card_data.copy()# 使用 copy() 方法創建副本
usingCardData.append('')  
for i in range(0, len(usingCardData)):
    if usingCardData[i] != '' and i< len(usingCardData):
        for j in range(1, 5):
            if i+j< len(usingCardData) and usingCardData[i+j] == '':
                n+=1
            elif i+j< len(usingCardData) and usingCardData[i+j] != '' and i+j>0:
                speace.append(n+1)
                n=0
                break
    elif i==len(usingCardData)-1:
        if usingCardData[i-1] != '':
            speace.append(1)
        elif usingCardData[i-2] != '':
            speace.append(2)
        elif usingCardData[i-3] != '':
            speace.append(3)
        elif usingCardData[i-4] != '':
            speace.append(4)
            
    
        
        
        
# 打印抓取到的數據
card_data = [text for text in card_data if text.strip()]

img_url ="https://ws-tcg.com/cardlist/"
driver = webdriver.Chrome(service=Service("C:/chromedriver-win64/chromedriver.exe"), options=options)
driver.get(img_url)

try:
    # 等待主元素加載
    body = WebDriverWait(driver, delay_time).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    site = body.find_element(By.ID, "site")
    site_main = site.find_element(By.CLASS_NAME, "site-main")
    site_content = site_main.find_element(By.CLASS_NAME, "site-content")
    site_content_inner = site_content.find_element(By.CLASS_NAME, "site-content-inner")
    entry_content = site_content_inner.find_element(By.CLASS_NAME, "entry-content")
    search_form = entry_content.find_element(By.ID, "searchForm")
    card_search_table = search_form.find_element(By.CLASS_NAME, "card-search-table")
    tbody = card_search_table.find_element(By.TAG_NAME, "tbody")
    tr = tbody.find_element(By.TAG_NAME, "tr")
    td = tr.find_element(By.TAG_NAME, "td")
    label = tbody.find_element(By.TAG_NAME, "label")
    input = tbody.find_element(By.TAG_NAME, "input")

    button = search_form.find_element(By.CSS_SELECTOR, 'input[name="button"]')
    
    input.send_keys(card_data[0])
    button.click()

    for i in range(1, len(card_data)+1):
        
        body = WebDriverWait(driver, delay_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        site = body.find_element(By.ID, "site")
        site_main = site.find_element(By.CLASS_NAME, "site-main")
        site_content = site_main.find_element(By.CLASS_NAME, "site-content")
        site_content_inner = site_content.find_element(By.CLASS_NAME, "site-content-inner")
        entry_content = site_content_inner.find_element(By.CLASS_NAME, "entry-content")
        
        contents_box_main = entry_content.find_element(By.TAG_NAME, "div")
        search_results = contents_box_main.find_element(By.TAG_NAME, "div")

        search_results_container = WebDriverWait(search_results, delay_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-result-table-container"))
        )
        search_result_table = search_results_container.find_element(By.TAG_NAME, "table")
        tbody = search_result_table.find_element(By.TAG_NAME, "tbody")
        tr = tbody.find_element(By.TAG_NAME, "tr")
        
        th = tr.find_element(By.TAG_NAME, "th")
        a = th.find_element(By.TAG_NAME, "a")
        img = a.find_element(By.TAG_NAME, "img")
       
        img_url = img.get_attribute("src")  # 取得圖片 URL
        save_path = os.path.join("C:/Users/wei/Documents/WsCard_png", f"card_{i}.jpg")  # 可依照需求自訂命名
        download_image(img_url, save_path)  # 下載圖片


        search_form = entry_content.find_element(By.ID, "searchForm")
        card_search_table = search_form.find_element(By.CLASS_NAME, "card-search-table")
        tbody = card_search_table.find_element(By.TAG_NAME, "tbody")
        tr = tbody.find_element(By.TAG_NAME, "tr")
        td = tr.find_element(By.TAG_NAME, "td")
        label = tbody.find_element(By.TAG_NAME, "label")
        input = tbody.find_element(By.TAG_NAME, "input")
        input.clear()
        input.send_keys(card_data[i])

        button = WebDriverWait(search_form, delay_time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="button"]'))
        )
        button.click()
        
        

        # 等待搜索結果加載
        
        

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # 關閉瀏覽器
    driver.quit()






# 目標圖片尺寸（寬, 高），可依需求調整
A4_WIDTH_CM = 21.0
A4_HEIGHT_CM = 29.7
DPI = 300

# 卡片尺寸（你提供的：6.47cm x 9.02cm）
CARD_WIDTH_CM = 6.47
CARD_HEIGHT_CM = 9.02

# 換算為像素
a4_width_px = int(A4_WIDTH_CM / 2.54 * DPI)
a4_height_px = int(A4_HEIGHT_CM / 2.54 * DPI)
card_width_px = int(CARD_WIDTH_CM / 2.54 * DPI)
card_height_px = int(CARD_HEIGHT_CM / 2.54 * DPI)


cols = floor(a4_width_px / card_width_px)
rows = floor(a4_height_px / card_height_px)
cards_per_page = cols * rows

images = []
e_count = 0
# 排序圖片檔案名稱，按數字順序
image_files = sorted(
    [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
    key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf')
)

for i, count in enumerate(speace):
    if i >= len(image_files):
        break
    img_path = os.path.join(image_folder, image_files[i])
    img = Image.open(img_path).convert("RGB")
    e_count = count + e_count

    if len(usingCardData)>=50 and e_count <= 8:
        # 前 8 張旋轉 180 度並對調長寬
        img = img.rotate(90, expand=True)
        img = img.resize((card_width_px, card_height_px), Image.LANCZOS)
    else:
        img = img.resize((card_width_px, card_height_px), Image.LANCZOS)

    # 根據 count 數量複製卡片
    for _ in range(count):
        images.append(img.copy())

# === 將圖片排列成多頁 PDF ===
pages = []
for i in range(0, len(images), cards_per_page):
    page_img = Image.new("RGB", (a4_width_px, a4_height_px), "white")
    for index_on_page, img in enumerate(images[i:i + cards_per_page]):
        row = index_on_page // cols
        col = index_on_page % cols
        x = col * card_width_px
        y = row * card_height_px
        page_img.paste(img, (x, y))
    pages.append(page_img)

# === 輸出 PDF ===
if pages:
    pages[0].save(output_pdf_path, save_all=True, append_images=pages[1:])
    print(f"✅ PDF 已儲存：{output_pdf_path}")
else:
    print("⚠️ 沒有圖片可處理。") 
    
