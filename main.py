from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("useAutomationExtension", False)
service = ChromeService(executable_path="C:/Windows/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
import pandas
import time

# Variables
product_url = []
product_name = []
price = []
product_rating = []

def product_info(no_of_pages):
    driver.get("https://www.cdiscount.com/bricolage/climatisation/traitement-de-l-air/ioniseur/l-166130303.html#_his_")
    count_page = 0
    while count_page != no_of_pages:
        time.sleep(20)
        # Product link
        url_path = driver.find_elements(By.XPATH, '//*[@id="lpBloc"]//li/a')
        for item in url_path:
            product_url.append(item.get_attribute("href"))

        # Product name
        name_path = driver.find_elements(By.XPATH, '//*[@class="prdtTit"]')
        for name in name_path:
            product_name.append(name.text)

        # Product price
        price_path = driver.find_elements(By.XPATH, '//*[@class="priceLine"]')
        for pro_price in price_path:
            price.append(pro_price.text)
        
        # Product Rating
        rating_path = driver.find_elements(By.XPATH, '//*[@class="productDescZone"]')
        for rate in rating_path:
            try:
                product_rating.append(rate.find_element(By.CLASS_NAME, "prdtBStar").find_element(By.TAG_NAME, "span").get_attribute("innerHTML"))
            except:
                product_rating.append("Not present")

        try:
            driver.get(driver.find_element(By.CLASS_NAME, "jsNxtPage").get_attribute("href"))
            if count_page <= no_of_pages:
                count_page += 1
            else:
                break
        except:
            break


        print(f"Scrapped Page: {count_page}")

def main():
    user_input = int(input("How many pages do you wish to scrape?(1-274): "))
    print("Scraping data...")
    product_info(user_input)
    driver.close()
    
    # Write data to csv
    print("Writing data to file ...")
    df = pandas.DataFrame({"URL":product_url,"Name":product_name,"Price_in_EUR":price,"Ratings":product_rating})
    df.to_csv("cdiscount_data.csv", index=False)
    print("Finished.")

if __name__=='__main__':
    main()