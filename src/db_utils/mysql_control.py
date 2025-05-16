import mysql.connector
from tabulate import tabulate
import pandas as pd 
import os
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)
cursor = db.cursor()


def create_database_if_not_exists():
    cursor.execute("CREATE DATABASE IF NOT EXISTS sql_selenium_test_project")
    print("資料庫 'sql_selenium_test_project' 檢查完畢（存在或已建立）")

    # 切換到這個資料庫
    cursor.execute("USE sql_selenium_test_project")

def rename_table(old_name, new_name):
    cursor.execute(f"RENAME TABLE {old_name} TO {new_name}")
    print(f"Table renamed from {old_name} to {new_name}")


def insert_product(table_name, product_data):
    # 1️⃣ 先寫入主表
    sql_main = f"""
    INSERT INTO {table_name} (product_url, title, description, stars, reviews, price_128, price_256, price_512, price_1024)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        title=VALUES(title),
        description=VALUES(description),
        stars=VALUES(stars),
        reviews=VALUES(reviews),
        price_128=VALUES(price_128),
        price_256=VALUES(price_256),
        price_512=VALUES(price_512),
        price_1024=VALUES(price_1024)
    """
    values = (
        product_data["product_url"],
        product_data["title"],
        product_data["description"],
        product_data["stars"],
        product_data["reviews"],
        product_data["price_128"],
        product_data["price_256"],
        product_data["price_512"],
        product_data["price_1024"],
    )
    cursor.execute(sql_main, values)

    # 2️⃣ 再寫入歷史表 (products_laptops_history or products_tablets_history)
    history_table = table_name + "_history"
    sql_history = f"""
    INSERT INTO {history_table} (product_url, title, description, stars, reviews, price_128, price_256, price_512, price_1024)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_history, values)

    db.commit()


def insert_phone_product(table_name, product_data):
    # 1️⃣ 先寫入主表
    sql_main = f"""
    INSERT INTO {table_name} (product_url, title, description, stars, reviews, price)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        title=VALUES(title),
        description=VALUES(description),
        stars=VALUES(stars),
        reviews=VALUES(reviews),
        price=VALUES(price)
    """
    values = (
        product_data["product_url"],
        product_data["title"],
        product_data["description"],
        product_data["stars"],
        product_data["reviews"],
        product_data["price"],
    )
    cursor.execute(sql_main, values)

    # 2️⃣ 再寫入歷史表 (products_touch_phones_history)
    history_table = table_name + "_history"
    sql_history = f"""
    INSERT INTO {history_table} (product_url, title, description, stars, reviews, price)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_history, values)

    db.commit()



def create__history_tables():
    # 創建 products_touch_phones_history 表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_touch_phones_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_url VARCHAR(255) NOT NULL,
        title VARCHAR(255),
        description TEXT,
        stars FLOAT,
        reviews INT,
        price DECIMAL(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 創建 products_laptops_history 表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_laptops_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_url VARCHAR(255) NOT NULL,
        title VARCHAR(255),
        description TEXT,
        stars FLOAT,
        reviews INT,
        price_128 DECIMAL(10,2),
        price_256 DECIMAL(10,2),
        price_512 DECIMAL(10,2),
        price_1024 DECIMAL(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 創建 products_tablets_history 表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_tablets_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_url VARCHAR(255) NOT NULL,
        title VARCHAR(255),
        description TEXT,
        stars FLOAT,
        reviews INT,
        price_128 DECIMAL(10,2),
        price_256 DECIMAL(10,2),
        price_512 DECIMAL(10,2),
        price_1024 DECIMAL(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)



def create_products_laptops_TABLE(): #products_laptops 
    #建立DATABESE然後使用他#
    cursor.execute("CREATE DATABASE IF NOT EXISTS sql_selenium_test_project")
    cursor.execute("USE sql_selenium_test_project")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_laptops (
        product_url VARCHAR(255) PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        stars INT,
        reviews INT,
        price_128 DECIMAL(10,2),
        price_256 DECIMAL(10,2),
        price_512 DECIMAL(10,2),
        price_1024 DECIMAL(10,2)
    )
    """)

def create_products_tablets_TABLE(): #products_tablets 
    #建立DATABESE然後使用他#
    cursor.execute("CREATE DATABASE IF NOT EXISTS sql_selenium_test_project")
    cursor.execute("USE sql_selenium_test_project")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_tablets (
        product_url VARCHAR(255) PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        stars INT,
        reviews INT,
        price_128 DECIMAL(10,2),
        price_256 DECIMAL(10,2),
        price_512 DECIMAL(10,2),
        price_1024 DECIMAL(10,2)
    )
    """)


def create_products_touch_phones_TABLE():
    # 建立 DATABASE 然後使用它
    cursor.execute("CREATE DATABASE IF NOT EXISTS sql_selenium_test_project")
    cursor.execute("USE sql_selenium_test_project")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_touch_phones (
        product_url VARCHAR(255) PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        stars INT,
        reviews INT,
        price DECIMAL(10,2)
    )
    """)

def drop_TABLE():
    cursor.execute("USE sql_selenium_test_project")

    tables_to_drop = [
        "products_laptops",
        "products_laptops_history",
        "products_tablets",
        "products_tablets_history",
        "products_touch_phones",
        "products_touch_phones_history"
    ]

    for table in tables_to_drop:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")



def show_all_products():
    cursor.execute("USE sql_selenium_test_project")

    # 主表: Laptops
    print("\n==== 📚 products_laptops 資料 ====")
    cursor.execute("SELECT * FROM products_laptops")
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    print(tabulate(rows, headers, tablefmt="fancy_grid"))

    # 歷史表: Laptops
    print("\n==== 🕘 products_laptops_history 歷史資料 ====")
    cursor.execute("SELECT * FROM products_laptops_history")
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    print(tabulate(rows, headers, tablefmt="fancy_grid"))

    # 主表: Tablets
    print("\n==== 📚 products_tablets 資料 ====")
    cursor.execute("SELECT * FROM products_tablets")
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    print(tabulate(rows, headers, tablefmt="fancy_grid"))

    # 歷史表: Tablets
    print("\n==== 🕘 products_tablets_history 歷史資料 ====")
    cursor.execute("SELECT * FROM products_tablets_history")
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    print(tabulate(rows, headers, tablefmt="fancy_grid"))

    # 主表: Touch Phones
    print("\n==== 📚 products_touch_phones 資料 ====")
    cursor.execute("SELECT * FROM products_touch_phones")
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    print(tabulate(rows, headers, tablefmt="fancy_grid"))

    # 歷史表: Touch Phones
    print("\n==== 🕘 products_touch_phones_history 歷史資料 ====")
    cursor.execute("SELECT * FROM products_touch_phones_history")
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    print(tabulate(rows, headers, tablefmt="fancy_grid"))



def close_connection():
    cursor.close()
    db.close()


def export_all_tables_to_excel(connection, output_file_name):
    """
    將所有資料表匯出為 Excel，輸出至專案根目錄下的 data/excel_file 資料夾中

    :param connection: MySQL 資料庫連線
    :param output_file_name: 輸出的 Excel 檔名（例如 'export.xlsx'）
    """
    import pandas as pd
    import os

    cursor = connection.cursor()

    # 查詢所有表格名稱
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # 取得專案根目錄（src 的上層）
    current_file = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(current_file, "..", "..", ".."))

    # data/excel_file 資料夾路徑
    excel_dir = os.path.join(project_root, "data", "excel_file")
    os.makedirs(excel_dir, exist_ok=True)

    # 組成完整的 Excel 輸出路徑
    output_path = os.path.join(excel_dir, output_file_name)

    # 寫入 Excel 檔
    with pd.ExcelWriter(output_path) as writer:
        for (table_name,) in tables:
            df = pd.read_sql(f"SELECT * FROM {table_name}", con=connection)
            df.to_excel(writer, sheet_name=table_name, index=False)

    cursor.close()
    print(f"✅ 所有表格已成功匯出至：{output_path}")

# show_all_products()
# export_all_tables_to_excel(db, 'sql_selenium_test_project_export.xlsx')
# drop_TABLE()
# # create_products_laptops_TABLE()
# # create_products_tablets_TABLE()
# # create_products_touch_phones_TABLE()
# # find_product_by_title('Asus ROG Strix SCAR Edition GL503VM-ED115T')
# # rename_table('products', 'products_laptops')
# # create__history_tables()

