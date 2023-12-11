
from flask import Flask, request, jsonify
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException, StaleElementReferenceException
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
s1 = Service(ChromeDriverManager().install())
tls = threading.local()
def scrape_website(link, budget, pro_name, spec_list, s1, op):
    local_bestbuy_list = []
    local_e_list = []
    local_amazon_list = []
    if link == 'https://www.bestbuy.ca/en-ca':
        try:
            driver_bestbuy = webdriver.Chrome(service=s1, options=op)
            driver_bestbuy.get(link)
            driver_bestbuy.find_element(By.XPATH, '//input[@class="textField_XaJoz"]').send_keys(pro_name)
            driver_bestbuy.find_element(By.XPATH, '//button[@class="searchButton_2mES- fitContainer_2HpHA"]').click()
            driver_bestbuy.implicitly_wait(2.5)
            products_2 = driver_bestbuy.find_elements(By.XPATH, '//div[@class="col-xs-12_198le col-sm-4_13E9O col-lg-3_ECF8k x-productListItem productLine_2N9kG"]')
            for product in products_2:
                b_counter = 0
                try:
                    description_2 = product.find_element(By.XPATH, './/div[@class="productItemName_3IZ3c"]')
                    a_bool = True
                except:
                    a_bool = False
                try:
                    link_2 = product.find_element(By.XPATH, './/div/a')
                    link_2_ref = link_2.get_attribute('href')
                    b_bool = True
                except:
                    b_bool = False
                try:
                    price_2 = product.find_element(By.XPATH, './/span[@class="screenReaderOnly_2mubv large_3uSI_"]')
                    c_bool = True
                except:
                    c_bool = False

                p_cost = str(price_2.text).replace('$', '')
                p_total = float(p_cost)
                if len(spec_list) != 0:
                    p_description_2 = str(description_2.text).lower().replace('-', '').split()
                    for spec in spec_list:
                        if spec.lower() in p_description_2:
                            b_counter += 1
                        else:
                            pass
                    if b_counter > 1:
                        d_present = True
                    else:
                        d_present = False
                    if p_total < budget and d_present:
                        if a_bool and b_bool and c_bool:
                            b_obj = {"Description": f"{description_2.text}",
                                     "Price": f"{price_2.text}",
                                     "link": f"{link_2_ref}"
                                     }
                            local_bestbuy_list.append(b_obj)
                        else:
                            pass
                    else:
                        pass
                elif len(spec_list) == 0:
                    if p_total < budget:
                        if a_bool and b_bool and c_bool:
                            b_obj = {"Description": f"{description_2.text}",
                                     "Price": f"{price_2.text}",
                                     "link": f"{link_2_ref}"
                                     }
                            local_bestbuy_list.append(b_obj)
                        else:
                            pass
                    else:
                        pass
            driver_bestbuy.close()
        except NoSuchElementException:
            driver_bestbuy.close()
        except NoSuchAttributeException:
            driver_bestbuy.close()
        except TimeoutException:
            driver_bestbuy.close()
        except StaleElementReferenceException:
            driver_bestbuy.close()
    elif link == 'https://www.ebay.ca/':
        try:
            driver_ebay = webdriver.Chrome(service=s1, options=op)
            driver_ebay.get(link)
            driver_ebay.find_element(By.ID, 'gh-ac').send_keys(pro_name)
            driver_ebay.find_element(By.ID, 'gh-btn').click()
            driver_ebay.implicitly_wait(2)
            # WebDriverWait(driver_ebay, 3).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//li[@class="s-item s-item__pl-on-bottom"]')))
            products_4 = driver_ebay.find_elements(By.XPATH, '//li[@class="s-item s-item__pl-on-bottom"]')
            for product in products_4:
                e_counter = 0
                try:
                    description_4 = product.find_element(By.XPATH, './/div[@class="s-item__title"]/span')
                    d_bool = True
                except:
                    d_bool = False
                try:
                    link_4 = product.find_element(By.XPATH, './/a[@class="s-item__link"]')
                    link_4_ref = link_4.get_attribute('href')
                    l_bool = True
                except:
                    l_bool = False

                try:
                    price_4 = product.find_element(By.XPATH,
                                                   './/div[@class="s-item__detail s-item__detail--primary"]/span')
                    p_cost = str(price_4.text).replace('C', '').replace('$', '').strip()
                    p_total = float(p_cost)
                    p_bool = True
                except:
                    p_bool = False

                if len(spec_list) != 0:
                    p_description_4 = str(description_4.text).lower().replace('-', '').split()
                    for spec in spec_list:
                        if spec.lower() in p_description_4:
                            e_counter += 1
                        else:
                            pass
                    if e_counter > 1:
                        e_present = True
                    else:
                        e_present = False
                    if p_bool:
                        if e_present and p_total < budget:
                            if d_bool and l_bool:
                                local_e_list.append(
                                    {"Description": f"{description_4.text}", "Price": f"{p_cost}", "link": f"{link_4_ref}"})
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                elif len(spec_list) == 0:
                    if p_bool:
                        if p_total < budget:
                            if d_bool and l_bool:
                                local_e_list.append(
                                    {"Description": f"{description_4.text}", "Price": f"{p_cost}", "link": f"{link_4_ref}"})
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
            driver_ebay.close()

        except NoSuchElementException:
            driver_ebay.close()
        except NoSuchAttributeException:
            driver_ebay.close()
        except TimeoutException:
            driver_ebay.close()
        except StaleElementReferenceException:
            driver_ebay.close()

    elif link == "https://www.amazon.ca/":
        try:
            driver_amazon = webdriver.Chrome(service=s1, options=op)
            driver_amazon.get(link)
            driver_amazon.find_element(By.NAME, 'field-keywords').send_keys(pro_name)
            clickable = driver_amazon.find_element(By.ID, 'nav-search-submit-button')
            clickable.click()
            driver_amazon.implicitly_wait(1.6)
            products_1 = driver_amazon.find_elements(By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')
            for product in products_1:
                counter = 0
                try:
                    description_1 = product.find_element(By.XPATH,
                                                         './/span[@class="a-size-base-plus a-color-base a-text-normal"]')
                    des_bool = True
                except:
                    des_bool = False

                try:
                    whole_price = product.find_element(By.XPATH, './/span[@class="a-price-whole"]')
                    fraction_price = product.find_element(By.XPATH, './/span[@class="a-price-fraction"]')
                    if whole_price and fraction_price:
                        price_bool = True
                except:
                    price_bool = False

                try:
                    link_1 = product.find_element(By.XPATH, './/div[@class= "a-section a-spacing-none a-spacing-top-small s-title-instructions-style"]/h2/a')
                    link_1_ref = link_1.get_attribute('href')
                    link_bool = True
                except:
                    link_bool = False
                price_1 = int(whole_price.text)
                if len(spec_list) != 0:
                    p_description_1 = str(description_1.text).lower().replace('-', ' ').split()
                    for spec in spec_list:
                        if spec.lower() in p_description_1:
                            counter += 1
                        else:
                            pass
                    if counter > 1:
                        is_present = True
                    else:
                        is_present = False
                    if price_1 < budget and is_present:
                        if price_bool and des_bool and link_bool:
                            result_object = {
                                "Description": f"{description_1.text}",
                                "Price": f"{whole_price.text}.{fraction_price.text}",
                                "link": f"{link_1_ref}"
                            }
                            local_amazon_list.append(result_object)
                        else:
                            pass
                    else:
                        pass

                elif len(spec_list) == 0:
                    if price_1 < budget:
                        if price_bool and des_bool and link_bool:
                            result_object = {
                                "Description": f"{description_1.text}",
                                "Price": f"{whole_price.text}.{fraction_price.text}",
                                "link": f"{link_1_ref}"
                            }
                            local_amazon_list.append(result_object)
                        else:
                            pass
                    else:
                        pass
            driver_amazon.close()

        except TimeoutException:
            driver_amazon.close()
        except NoSuchElementException:
            driver_amazon.close()
        except NoSuchAttributeException:
            driver_amazon.close()
        except UnboundLocalError:
            driver_amazon.close()
        except ValueError:
            driver_amazon.close()
    


    # Return local lists
    return local_bestbuy_list, local_e_list, local_amazon_list

@app.route('/', methods=['POST'])
def start():
    request_data = request.get_json()
    product_name = request_data.get('p_name')
    budget = request_data.get('b_name')
    f_bug = int(budget)
    att_list = request_data.get('speclist')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
    }
    urls = ['https://www.amazon.ca/', 'https://www.ebay.ca/', 'https://www.bestbuy.ca/en-ca']
    op = Options()
    op.add_argument('--disable-blink-features=AutomationControlled')
    profile = {
        'profile.default_content_setting_values': {
            'images': 2,  # Block images
            'popups': 2,  # Block pop-ups
            'geolocation': 2,  # Block geolocation
            'notifications': 2  # Block notifications
        }
    }
    # op.add_argument("--headless")
    # chrome_prefs = {"profile.managed_default_content_settings.images": 2}
    op.add_experimental_option("prefs", profile)

    for key, value in headers.items():
        op.add_argument(f"--{key}={value}")

    with ThreadPoolExecutor() as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(scrape_website, url, f_bug, product_name, att_list, s1, op))

    # Initialize local result lists
    local_bestbuy_list = []
    local_e_list = []
    local_amazon_list = []

    for future in futures:
        bestbuy_list, e_list, amazon_list = future.result()
        local_bestbuy_list.extend(bestbuy_list)
        local_e_list.extend(e_list)
        local_amazon_list.extend(amazon_list)

    new_obj = {"list_1": local_bestbuy_list, "list_2": local_e_list, "list_3": local_amazon_list}
    return jsonify(new_obj)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
