from functions import *
from driver_utils import driver_setting
# from driver_setting import *
import time
from db_utils.mysql_control import (
    db,
    create_database_if_not_exists,
    create_products_laptops_TABLE,
    create_products_tablets_TABLE,
    create_products_touch_phones_TABLE,
    create__history_tables,
    show_all_products,
    export_all_tables_to_excel
)

if __name__ == "__main__":

    # Step 1: 預先建立資料表（僅當不存在時建立）
    create_database_if_not_exists()
    create_products_laptops_TABLE()
    create_products_tablets_TABLE()
    create_products_touch_phones_TABLE()
    create__history_tables()

    # Step 2: 啟動瀏覽器並執行爬蟲
    driver = driver_setting.get_driver()
    navigate_to_ecommerce(driver)

    # Laptops
    go_to_laptops_page(driver)
    scrap_all_pages(driver, category="laptops", start_page=1, end_page=20)
    time.sleep(1.5)

    # Tablets
    go_to_tablets_page(driver)
    scrap_all_pages(driver, category="tablets", start_page=1, end_page=4)
    time.sleep(1.5)

    # Touch phones
    go_to_touch_phones_page(driver)
    scrap_all_pages(driver, category="touch_phones", start_page=1, end_page=2)

    driver.quit()

    # Step 3: 顯示資料並匯出 Excel
    show_all_products()
    export_all_tables_to_excel(db, 'sql_selenium_test_project_export.xlsx')