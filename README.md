# 📦 sql_selenium_test_project

本專案使用 Python + Selenium 建立自動化爬蟲，針對電子商務網站(https://webscraper.io/test-sites/e-commerce/ajax)上的 **筆記型電腦 / 平板 / 觸控手機** 商品進行爬取，並將資料儲存至 MySQL 資料庫，最後匯出為 Excel 檔案。

---

## 🚀 專案功能

- ✅ 自動前往電子商務網站指定分類頁
- ✅ 分頁爬取商品資訊（名稱、價格、描述、評價等）
- ✅ 根據商品分類自動寫入對應 MySQL 資料表
- ✅ 匯出所有表格為 Excel 檔案
- ✅ 自動建立資料表（若不存在）

---

## 📁 專案結構

sql_selenium_test_project/
├── data/
│ └── excel_file/ # 匯出結果儲存處（自動建立）
├── src/
│ ├── main.py # 主程式，執行完整爬蟲流程
│ ├── functions.py # 所有爬蟲相關功能與流程
│ ├── config.py # 設定參數（如連線字串、選單路徑等）
│ ├── db_utils/
│ │ └── mysql_control.py # MySQL 操作：建表、寫入、匯出等
│ └── driver_utils/
│ ├── driver_setting.py # 建立與設定 Selenium WebDriver
│ └── driver/
│ └── chromedriver.exe # ChromeDriver 執行檔
├── requirements.txt # 所需安裝套件列表
└── README.md # 專案說明文件（本檔案）

## 前置準備
1. 安裝好 MySQL 並建立資料庫：sql_selenium_test_project

2. 確保在 mysql_control.py 中的連線資訊（host, user, password）正確

3. 將 chromedriver.exe 放在 src/driver_utils/driver/ 中

## 執行方式
在專案根目錄中執行：python src/main.py


## 匯出結果
data/excel_file/sql_selenium_test_project_export.xlsx
