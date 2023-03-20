import requests
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://www.lycamobile.us/en/checkout/'

phone_number = "9172147726"
# action=get_plan_details&mobile_number=9172147727
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    driver = selenium.webdriver.Chrome('./webdriver/chromedriver.exe', options=chrome_options)
    return driver

def scrape(driver, url, phone): 
    driver.get(url)
    driver.implicitly_wait(12)
    driver.find_element(By.XPATH, '//*[@id="nc_topup_mobile_no"]').send_keys(phone)
    time.sleep(5)
    resp = driver.find_element(By.XPATH, '//*[@id="nc_mb_error"]').get_attribute('style')
    if resp == "display: none;":
        return True
    elif resp == "display: block;":
        return False
    return None

def save(number):
    with open("results.txt", "a") as f:
        f.write(number + "\n")

def get_counter():
    try:
        with open("place", "r") as f:
            return int(f.read())
    except:
        return 0

def main():
    global counter
    base = "917214"
    counter = get_counter()
    driver = get_driver()
    while counter < 10000:
        if len(str(counter)) <= 4:
            needed = 4 - len(str(counter))
            adding = ''.join(['0'for i in range(needed)]) + str(counter)
        phone_number = base + adding
        print(f"Trying {phone_number}...")
        re = scrape(driver, url, phone_number)
        if re == True:
            save(phone_number)
        elif re == False:
            print("Not a valid number")
        elif re == None:
            print("Error")
        counter += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        with open("place", "w") as f:
            f.write(str(counter))

# re = requests.post(url, data={'action': 'get_plan"details', 'mobile_number': phone_number}, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest"})
# with open("out.html", "w") as out:
#     out.write(re.text)

# print(re.json())