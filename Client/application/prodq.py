from selenium import webdriver
import chromedriver_autoinstaller
import time
from bs4 import BeautifulSoup
chromedriver_autoinstaller.install()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import requests

class AmazonQuery():
    @staticmethod
    def SearchProducts(query:str):
        search = query
        co = Options()
        co.add_argument("--headless")
        co.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options= co)
        tz_params = {'timezoneId': 'UTC'}
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
        driver.get(f"https://www.amazon.in/s?k={search}")
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source , "html.parser")
        with open("output1.html", "w", encoding='utf-8') as file:
            file.write(str(soup))
        r1 = soup.find("div" , {"data-cel-widget" : "search_result_2"})
        r2 = soup.find("div" , {"data-cel-widget" : "search_result_3"})
        s1,s2 = None,None
        if(r1):
            s1 = soup.find("div" , {"data-cel-widget" : "search_result_2"}).get("data-asin")
        if(r2):
            s2 = soup.find("div" , {"data-cel-widget" : "search_result_3"}).get("data-asin")

        return [s1,s2]

    @staticmethod
    def GetProductInfo(asin:str):
        co = Options()
        co.add_argument("--headless")
        co.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options= co)
        tz_params = {'timezoneId': 'UTC'}
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
        driver.get(f"https://www.amazon.in/dp/{asin}")
        try:
            myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'landingImage')))
        except TimeoutException:
            try:
                myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'img-canvas')))
            except TimeoutException:
                return AmazonQuery.GetProductInfo(asin)
        soup = BeautifulSoup(driver.page_source , "html.parser")
        with open("output1.html", "w", encoding='utf-8') as file:
            file.write(str(soup))
        title = soup.find("span" , {"id" : "productTitle"}).text.strip()
        try:
            img = soup.find("img" , {"id" : "landingImage"}).get("src")
        except:
            img = soup.find("div" , {"id" : "img-canvas"}).find_all("img")[-1].get("src")
        price = soup.find("span" , {"class":"a-price-whole"}).text
        stars = soup.find("div" , {"id":"averageCustomerReviews"}).span.span.get("title")
        return {"ASIN":asin , "title":title,"img":img,"price":price,"stars":stars}

class FlipkartQuery():
    @staticmethod
    def SearchProducts(query:str):
        try:
            r = requests.get(f'https://flipkart.dvishal485.workers.dev/search/{query}')
            return [r.json()["result"][0],r.json()["result"][1]]
        except:
            time.sleep(1)
            print("Fail Flipkart Search")
            return FlipkartQuery.SearchProducts(query)
    
    @staticmethod
    def GetProductID(query_url):
        try:
            r = requests.get(query_url)
            return r.json()["product_id"]
        except:
            time.sleep(1)
            return FlipkartQuery.GetProductID(query_url)
    
    @staticmethod
    def GetProductRating(query_url):
        try:
            r = requests.get(query_url)
            return int(r.json()["rating"])
        except:
            time.sleep(1)
            return FlipkartQuery.GetProductRating(query_url)
        
    @staticmethod
    def GetProductImage(query_url):
        try:
            r = requests.get(query_url)
            return int(r.json()["rating"])
        except:
            time.sleep(1)
            return FlipkartQuery.GetProductImage(query_url)
    

