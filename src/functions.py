from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import config
from db_utils import mysql_control



def navigate_to_ecommerce(driver):
    try:
        driver.get(config.URL)
        driver.maximize_window()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"Successfully navigated to the new page: {config.URL}")
        time.sleep(3)
        
        # take_screenshot(driver, "e-commerce")

    except Exception as e:
        print(f"Error occurred in navigate_to_e-commerce: {e}")

def go_to_laptops_page(driver):
    try:
        computers_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config.COMPUTERS_LINK_XPATH))
                                                           
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", computers_link)
        time.sleep(0.5)  
        computers_link.click()
        time.sleep(1)
        laptops_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config.LAPTOPS_LINK_XPATH))
        )
        laptops_link.click()

    except Exception as e:
        print(f"Error occurred in navigate_to_e-commerce: {e}")

def go_to_tablets_page(driver):
    try:
        computers_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config.COMPUTERS_LINK_XPATH))
                                                           
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", computers_link)
        time.sleep(0.5)  
        computers_link.click()
        time.sleep(1)
        tablets_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config.TABELETS_LINK_XPATH))
        )
        tablets_link.click()
    except Exception as e:
        print(f"Error occurred in navigate_to_e-commerce: {e}")

def go_to_touch_phones_page(driver):
    try:
        phones_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config.PHONES_LINK_XPATH))
                                                           
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", phones_link)
        time.sleep(0.5)  
        phones_link.click()
        time.sleep(1)
        touch_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config.TOUCH_LINK_XPATH))
        )
        driver.execute_script("arguments[0].click();", touch_link)
        touch_link.click()

    except Exception as e:
        print(f"Error occurred in navigate_to_e-commerce: {e}")

def scrap_products_Laptops(driver):
    try:
        ###點擊接受COOKIE以防他擋我要點的元素###
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, config.ACCPET_BUTTON_CSS_SELECTOR))
            )
            accept_button.click()
            print("Clicked 'Accept & Continue' button.")
        except:
            print("No 'Accept & Continue' button found or already accepted.")

        # 等待並抓取所有產品元素 抓產品的href跟名稱並且回傳成list 
        #        [
        #     <selenium.webdriver.remote.webelement.WebElement (session="abc123", element="def456")>,
        #     <selenium.webdriver.remote.webelement.WebElement (session="abc123", element="ghi789")>,
        #     ...
        # ]

        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, config.PRODUCT_ELEMENTS_XPATH))
        )
        

        products = []
        for elem in product_elements:
            href = elem.get_attribute("href") #透過 .get_attribute() 去提取字串 去剛剛上面的去剛剛上面的product_elements 裡面提出字串
            name = elem.get_attribute("title") 
            products.append({"href": href, "name": name}) #把剛剛提取的 href 和 name(實際上是title的字串 只是剛剛回傳後取叫name) 塞進"href" "name" 這兩個 key 變成字典再加入到products這個list
        


        for product in products:
            href = product["href"] #https://webscraper.io/test-sites/e-commerce/ajax/product/518

            name = product["name"] #Lenovo ThinkPad 11e


        # 存 href 和 name，避免 stale element reference  因為當你點擊之後頁面會變，原本抓到的元素就會失效了，所以這裡先提取文字和網址出來
        #一個list裡面很多個字典
        # [
        #     {'href': 'https://webscraper.io/test-sites/e-commerce/ajax/product/518', 'name': 'Lenovo ThinkPad 11e'},
        #     {'href': 'https://webscraper.io/test-sites/e-commerce/ajax/product/519', 'name': 'Dell Inspiron 15'},
        #     ...
        # ]

        
            # 根據相對路徑創建 XPath
            relative_xpath = f"//a[@href='{href.replace('https://webscraper.io', '')}']"  #這邊要替換是因為下面這邊要替換是因為下面product_element 他要點及元素但她元素裡的href其實只有他要點及元素但她元素裡的href其實只有/test-sites/e-commerce/ajax/product/518 你給整串你給整串 https://webscraper.io/test-sites/e-commerce/ajax/product/518他抓不到

            product_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, relative_xpath))
            )
            product_element.click()  
            print(f"\n訪問產品: {name}")
            print(f"連結: {href}")
            time.sleep(1)
            #####step 1: 抓產品description#####
            try:
                desc_element = driver.find_element(By.XPATH, config.DESCRIPTION_XPATH) 
                description = desc_element.text
                print(f"產品描述: {description}")
            except Exception as e:
                print(f"抓描述失敗: {e}")
                description = "N/A"
            #####step 2: 抓幾顆星#####
            try:
                stars = driver.find_elements(By.XPATH, config.STARS_XPATH)
                star_count = len(stars)
                print(f"滿意度: {star_count} 顆星")
            except Exception as e:
                print(f"抓星星數失敗: {e}")
                star_count = 0  # 當作0顆
            #####step 3: 抓評論數#####
            try:
                review_count_element = driver.find_element(By.XPATH, config.REVIEW_COUNT_ELEMENT_XPATH)
                review_count = review_count_element.text
                print(f"評論數: {review_count}")
            except Exception as e:
                print(f"抓評論數失敗: {e}")
                review_count = "0"

            price_results = {}  
            #####step 4: 根據規格抓取價格#####
            for spec in config.SPEC_TO_CLICK:
                try:
                    # 用 XPath 根據 value 屬性找按鈕
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[@value='{spec}']"))
                    )
                    button.click()
                    
                    # 抓價格
                    price_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, config.PRICE_ELEMENT_XPATH))
                    )
                    price_text = price_element.text  # 例如 "$295.99"
                    price_value = float(price_text.replace('$', '').strip()) #去掉$
                    price_results[spec] = price_value  #像是前面有設list  SPEC_TO_CLICK = ["128", "256", "512", "1024"] for spec跑 所以假設這次128開始他會變成price_results[128] = 295.99  128會變成key 295.99會變成對應value
                    # {
                    # "128": 295.99,
                    # "256": 345.99,
                    # "512": 399.99,
                    # "1024": 489.99
                    # }


                    print(f"  點擊 {spec}，價格: {price_value}")
                    
                    time.sleep(1)
                except Exception as e:
                    print(f"  規格 {spec} 發生錯誤: {e}")
                    price_results[spec] = "N/A"

            ##### Step 5: 寫入 MySQL #####
            product_data = {
                "product_url": href,
                "title": name,
                "description": description,
                "stars": star_count,
                "reviews": review_count,
                "price_128": price_results.get("128", 0.0),
                "price_256": price_results.get("256", 0.0),
                "price_512": price_results.get("512", 0.0),
                "price_1024": price_results.get("1024", 0.0)
            }

            # 寫入你的 sql_test.py
            mysql_control.insert_product("products_laptops", product_data)
            print(f"✅ 已寫入資料庫: {name}")
            # 🔥 這裡可以把 price_results 寫入外層資料表 (如需存檔或輸出)

            driver.back()  # 回上一頁
            time.sleep(2)  # 等頁面載入回來

    except Exception as e:
        print(f"Error occurred in scrap_all_visible_products: {e}")

def scrap_products_Tablets(driver):
    try:
        ###點擊接受COOKIE以防他擋我要點的要素###
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, config.ACCPET_BUTTON_CSS_SELECTOR))
            )
            accept_button.click()
            print("Clicked 'Accept & Continue' button.")
        except:
            print("No 'Accept & Continue' button found or already accepted.")

        # 等待並抓取所有產品元素 抓產品的href跟名稱並且回傳成list 
        #        [
        #     <selenium.webdriver.remote.webelement.WebElement (session="abc123", element="def456")>,
        #     <selenium.webdriver.remote.webelement.WebElement (session="abc123", element="ghi789")>,
        #     ...
        # ]

        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, config.PRODUCT_ELEMENTS_XPATH))
        )
        
        # 存 href 和 name，避免 stale element reference  因為當你點擊之後頁面會變，原本抓到的元素就會失效了，所以這裡先提取文字和網址出來
        #一個list裡面很多個字典
        # [
        #     {'href': 'https://webscraper.io/test-sites/e-commerce/ajax/product/518', 'name': 'Lenovo ThinkPad 11e'},
        #     {'href': 'https://webscraper.io/test-sites/e-commerce/ajax/product/519', 'name': 'Dell Inspiron 15'},
        #     ...
        # ]

        products = []
        for elem in product_elements:
            href = elem.get_attribute("href") #透過 .get_attribute() 去提取字串 去剛剛上面的去剛剛上面的product_elements 裡面提出字串
            name = elem.get_attribute("title") 
            products.append({"href": href, "name": name}) #把剛剛提取的 href 和 name(實際上是title的字串 只是剛剛回傳後取叫name) 塞進"href" "name" 這兩個 key 變成字典再加入到products這個list
        


        for product in products:
            href = product["href"] #https://webscraper.io/test-sites/e-commerce/ajax/product/518

            name = product["name"] #Lenovo ThinkPad 11e


            # 根據相對路徑創建 XPath
            relative_xpath = f"//a[@href='{href.replace('https://webscraper.io', '')}']"  #這邊要替換是因為下面這邊要替換是因為下面product_element 他要點及元素但她元素裡的href其實只有他要點及元素但她元素裡的href其實只有/test-sites/e-commerce/ajax/product/518 你給整串你給整串 https://webscraper.io/test-sites/e-commerce/ajax/product/518他抓不到

            product_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, relative_xpath))
            )
            product_element.click()  
            print(f"\n訪問產品: {name}")
            print(f"連結: {href}")
            time.sleep(1)
            #####step 1: 抓產品description#####
            try:
                desc_element = driver.find_element(By.XPATH, config.DESCRIPTION_XPATH) 
                description = desc_element.text
                print(f"產品描述: {description}")
            except Exception as e:
                print(f"抓描述失敗: {e}")
                description = "N/A"
            #####step 2: 抓幾顆星#####
            try:
                stars = driver.find_elements(By.XPATH, config.STARS_XPATH)
                star_count = len(stars)
                print(f"滿意度: {star_count} 顆星")
            except Exception as e:
                print(f"抓星星數失敗: {e}")
                star_count = 0  # 當作0顆
            #####step 3: 抓評論數#####
            try:
                review_count_element = driver.find_element(By.XPATH, config.REVIEW_COUNT_ELEMENT_XPATH)
                review_count = review_count_element.text
                print(f"評論數: {review_count}")
            except Exception as e:
                print(f"抓評論數失敗: {e}")
                review_count = "0"

            price_results = {}  
            #####step 4: 根據規格抓取價格#####
            for spec in config.SPEC_TO_CLICK:
                try:
                    # 用 XPath 根據 value 屬性找按鈕
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[@value='{spec}']"))
                    )
                    button.click()
                    
                    # 抓價格
                    price_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, config.PRICE_ELEMENT_XPATH))
                    )
                    price_text = price_element.text  # 例如 "$295.99"
                    price_value = float(price_text.replace('$', '').strip()) #去掉$
                    price_results[spec] = price_value  #像是前面有設list  SPEC_TO_CLICK = ["128", "256", "512", "1024"] for spec跑 所以假設這次128開始他會變成price_results[128] = 295.99  128會變成key 295.99會變成對應value
                    # {
                    # "128": 295.99,
                    # "256": 345.99,
                    # "512": 399.99,
                    # "1024": 489.99
                    # }


                    print(f"  點擊 {spec}，價格: {price_value}")
                    
                    time.sleep(1)
                except Exception as e:
                    print(f"  規格 {spec} 發生錯誤: {e}")
                    price_results[spec] = "N/A"

            ##### Step 5: 寫入 MySQL #####
            product_data = {
                "product_url": href,
                "title": name,
                "description": description,
                "stars": star_count,
                "reviews": review_count,
                "price_128": price_results.get("128", 0.0),
                "price_256": price_results.get("256", 0.0),
                "price_512": price_results.get("512", 0.0),
                "price_1024": price_results.get("1024", 0.0)
            }

            # 寫入你的 sql_test.py
            mysql_control.insert_product("products_tablets", product_data)
            print(f"✅ 已寫入資料庫: {name}")
            # 🔥 這裡可以把 price_results 寫入外層資料表 (如需存檔或輸出)

            driver.back()  # 回上一頁
            time.sleep(2)  # 等頁面載入回來

    except Exception as e:
        print(f"Error occurred in scrap_all_visible_products: {e}")

def scrap_products_touch_phone(driver):
    try:
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, config.ACCPET_BUTTON_CSS_SELECTOR))
            )
            accept_button.click()
            print("Clicked 'Accept & Continue' button.")
        except:
            print("No 'Accept & Continue' button found or already accepted.")
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, config.PRODUCT_ELEMENTS_XPATH))
        )
        products = []
        for elem in product_elements:
            href = elem.get_attribute("href")
            name = elem.get_attribute("title")
            products.append({"href": href, "name": name})
        for product in products:
            href = product["href"]
            name = product["name"] 
            # 根據相對路徑創建 XPath
            relative_xpath = f"//a[@href='{href.replace('https://webscraper.io', '')}']"
            
            # 確保該產品鏈接可點擊
            product_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, relative_xpath))
            )
            product_element.click()  # 點擊鏈接
            print(f"\n訪問產品: {name}")
            print(f"連結: {href}")
            time.sleep(1)
            #####step 1: 抓產品description#####
            try:
                desc_element = driver.find_element(By.XPATH, config.DESCRIPTION_XPATH)
                description = desc_element.text
                print(f"產品描述: {description}")
            except Exception as e:
                print(f"抓描述失敗: {e}")
                description = "N/A"
            #####step 2: 抓幾顆星#####
            try:
                stars = driver.find_elements(By.XPATH, config.STARS_XPATH)
                star_count = len(stars)
                print(f"滿意度: {star_count} 顆星")
            except Exception as e:
                print(f"抓星星數失敗: {e}")
                star_count = 0  
            #####step 3: 抓評論數#####
            try:
                review_count_element = driver.find_element(By.XPATH, config.REVIEW_COUNT_ELEMENT_XPATH)
                review_count = review_count_element.text
                print(f"評論數: {review_count}")
            except Exception as e:
                print(f"抓評論數失敗: {e}")
                review_count = "0"

            price_results = [] 
            #####step 4: 根據規格抓取價格#####
            try:
                price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, config.PRICE_ELEMENT_XPATH))
                )
                price_text = price_element.text 
                price_value = float(price_text.replace('$', '').strip()) 
                price_results.append(price_value)

                print(f"  價格: {price_value}")
                
                time.sleep(1)
            except Exception as e:
                print(f"  發生錯誤: {e}")
                price_results = "N/A"
            ##### Step 5: 寫入 MySQL #####
            product_data = {
                "product_url": href,
                "title": name,
                "description": description,
                "stars": star_count,
                "reviews": review_count,
                "price": price_value  # 這次只存單一價格
            }

            # 寫入你的 sql_test.py
            mysql_control.insert_phone_product("products_touch_phones", product_data)
            print(f"✅ 已寫入資料庫: {name}")

            driver.back()  # 回上一頁
            time.sleep(2)  # 等頁面載入回來

    except Exception as e:
        print(f"Error occurred in scrap_products_touch_phone: {e}")

def scrap_all_pages(driver, category="laptops", start_page=1, end_page=20):
    try:
        current_page = start_page

        while current_page <= end_page:
            print(f"\n======== 現在處理第 {current_page} 頁 ========")

            # 根據 category 選擇要爬取的函數
            if category == "laptops":
                scrap_products_Laptops(driver)
            elif category == "tablets":
                scrap_products_Tablets(driver)
            elif category == "touch_phones":
                scrap_products_touch_phone(driver)

            if current_page < end_page:
                try:
                    # ✅ 找當前 active 頁碼按鈕
                    active_button = driver.find_element(By.XPATH, config.ACTIVE_BUTTON)
                    active_page_id = int(active_button.get_attribute("data-id"))

                    # ✅ 🚩 如果 active_page_id 已經到20（最大頁），停止
                    if active_page_id >= 20:
                        print("✅ 已到達最大頁數 20，停止爬取")
                        break

                    # ✅ 找下一頁按鈕 (data-id = active + 1)
                    next_button = driver.find_element(By.XPATH, f"//button[@data-id='{active_page_id + 1}']")
                    next_button.click()
                    time.sleep(2)

                except Exception as click_error:
                    print(f"❌ 找不到下一頁按鈕: {click_error}")
                    break

            current_page += 1

    except Exception as e:
        print(f"Error occurred in scrap_all_pages: {e}")
