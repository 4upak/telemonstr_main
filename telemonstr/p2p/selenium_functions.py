from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_data(driver):
    soup = BeautifulSoup(driver.page_source, "lxml")
    currencies = soup.find_all('div', class_='css-1m1f8hn')
    avalable = soup.select('div.css-1q1sp11 > div.css-lalzkr > div > div.css-3v2ep2 > div.css-vurnku')
    limits_from = soup.select(
        'div.css-1q1sp11 > div.css-lalzkr > div > div.css-16w8hmr > div.css-vurnku > div:nth-child(1)')
    limits_to = soup.select(
        'div.css-1q1sp11 > div.css-lalzkr > div > div.css-16w8hmr > div.css-vurnku > div:nth-child(3)')
    nicks = soup.find_all('a', {"id": "C2Cofferlistsell_link_merchant"})

    data = []
    i = 0
    for curr in currencies:
        data.append(
            {
                'nick': nicks[i].text,
                'avalable': float(avalable[i].text.replace(',', '').replace(' USDT', '')),
                'limits_from': float(limits_from[i].get_text().replace(',', '').replace('₴', '')),
                'limits_to': float(limits_to[i].get_text().replace(',', '').replace('₴', '')),
                'currencie': float(currencies[i].text)
            }
        )
        i += 1
    return data

def prepare_to_parse(driver):
    wait = WebDriverWait(driver, 10)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
    )
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    driver.execute_script('arguments[0].click()', button)


    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.css-ebuj64 path")))
    button.click()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-1m1f8hn"))
    )
    driver.implicitly_wait(30)
    time.sleep(5)
    return driver

def get_numbers(driver, url):
    driver.get(url)
    try:
        driver = prepare_to_parse(driver)
    except:
        print('Шото не клацнуло')

    data = get_data(driver)
    while len(data) == 0:
        print(f"Data lenght:{len(data)}")
        driver.refresh()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-1m1f8hn"))
        )
        driver.implicitly_wait(30)
        time.sleep(10)

        data = get_data(driver)

    total_volum_fiat = 0
    total_volum_crypto = 0
    ang_price = 0

    for item in data:
        total_volum_fiat = total_volum_fiat + item['currencie'] * item['avalable']
        total_volum_crypto = total_volum_crypto + item['avalable']

    ang_price = total_volum_fiat / total_volum_crypto

    r_total_volum_fiat = 0
    r_total_volum_crypto = 0
    new_data = data[6:]
    for item in new_data:
        r_total_volum_fiat = r_total_volum_fiat + item['currencie'] * item['avalable']
        r_total_volum_crypto = r_total_volum_crypto + item['avalable']

    recomend_ang_price = r_total_volum_fiat / r_total_volum_crypto



    data = {
        'total_volum_fiat':total_volum_fiat,
        'total_volum_crypto':total_volum_crypto,
        'avg_currencie':ang_price,
        'recomend_avg_price':recomend_ang_price,
        'avg_price':ang_price
    }
    return data