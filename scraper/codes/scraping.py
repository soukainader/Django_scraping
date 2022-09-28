from selenium.webdriver.edge.options import Options  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver  
from pymongo import MongoClient
from time import sleep
from lxml import html 
import pandas as pd
import cssselect
import pymongo
import webbrowser
import os
import time
import re

def scrap(dropdown,mylist,subject):
    start_time = time.time()
    #options = Options()
    #options.headless = False
    #driver = webdriver.Edge(executable_path=r"C:\Users\ADMIN\Desktop\msedgedriver.exe",options=options)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome('C:/Users/ADMIN/Desktop/chromedriver.exe',chrome_options=options)
    url ='https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText='+subject+'+&ltype=wholesale&SortType=total_tranpro_desc&page={}'
    
    client = MongoClient("mongodb://localhost:27017/")    
         # use variable db and collection names
    collection_name = subject
    collection = client["db2"][collection_name] 
    x = collection.delete_many({})   
    flg = True
    for page_nb in range(1, 2):
        
        print('---', page_nb, '---')    
        wait = WebDriverWait(driver, 10)
        actions = ActionChains(driver)
        driver.get(url.format(page_nb))
       
        #country_button = driver.find_element_by_class_name('ship-to')
        #country_button.click()
        #country_buttonn = driver.find_element_by_class_name('shipping-text')
        #country_buttonn.click()     
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='address-select-item ']//span[@class='shipping-text' and text()='Spain']"))).click()  
        #country_buttonnn = driver.find_element_by_class_name('ui-button ')
        #country_buttonnn.click() 
        sleep(2)
        current_offset = 0
        while True:
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            sleep(.5)  # JavaScript has time to add elements
            new_offset = driver.execute_script("return window.pageYOffset;")
            if new_offset <= current_offset:
                break
            current_offset = new_offset
        sleep(3)
        tree = html.fromstring(driver.page_source)
        results = []
        for product in tree.xpath('//div[@class="JIIxO"]//a'):
            title = product.xpath('.//h1/text()')
            if title:
                title = title[0]
                price = product.cssselect('div.mGXnE._37W_B span')
                leng = len(price)
                price = [x.text for x in price]

                currency = price[0]
                
                price = ''.join(price[1:])

                stars = product.xpath('.//span[@class="eXPaM"]/text()')
                if stars :
                    stars  = stars [0]
                else:
                    stars  = 'None'
                nb_sold = product.xpath('.//span[@class="_1kNf9"]/text()')
                if nb_sold:
                    nb_sold = nb_sold[0]
                else:
                    nb_sold = 'None'
                supl = product.xpath('.//a[@class="ox0KZ"]/text()')
                if supl:
                    supl = supl[0]
                else:
                    supl = 'None'
                ship_cost = product.xpath('.//span[@class="_2jcMA"]/text()')
                if ship_cost:
                    ship_cost = ship_cost[0]
                else:
                    ship_cost = 'None'
                product_links = product.xpath('./@href')
                if product_links:
                    product_links = str( product_links[0])
                row = [title, price, currency, stars, nb_sold, ship_cost, supl, product_links]
                results.append(row)
        # driver.close()-------Remove this code so driver is open and can open URL
        df = pd.DataFrame(results , columns=("Title","Price", "Currency", "Stars", "Orders", "Shipcost", "Supplier", "Productlinks" ))
        
        data = df.to_dict(orient = 'records')    
        
        collection.insert_many(data)  

def hello(dropdown,mylist,subject):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("start-maximized")
    driver = webdriver.Chrome('C:/Users/ADMIN/Desktop/chromedriver.exe',chrome_options=options)
    url1 ='https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText='+subject+'+&ltype=wholesale&SortType=total_tranpro_desc&page={}'

    client = MongoClient("mongodb://localhost:27017/")    
             # use variable db and collection names
    collection_name = subject
    collection = client["db2"][collection_name] 
    x = collection.delete_many({})   
    flg = True   
        
    
    for page_nb in range(1, 2): 
    
        print('---', page_nb, '---') 
    
        driver.get(url1.format(page_nb))
        urls = set()
        results = []
        for i in range(5):
            block = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/item/"]')]
            urls.update(block)
            driver.execute_script("window.scrollBy(0, arguments[0]);", 1200)
            time.sleep(2)
        for url in urls:
        
            driver.get(url)
            current_offset = 0
            while True:
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                sleep(.5)  # JavaScript has time to add elements
                new_offset = driver.execute_script("return window.pageYOffset;")
        
                try:
                        iframe = driver.find_element(By.CSS_SELECTOR, '#feedback iframe').get_attribute('src')
                except:
                        iframe = None
                if new_offset <= current_offset or iframe:
                    break
                current_offset = new_offset
        
            print(url)
            try: 
                title = driver.find_element(By.XPATH,'//h1[@class="product-title-text"]').text
                print (title) 
            except: 
                print ("none")
                
            try: 
                rating = driver.find_element(By.XPATH,'//span[@class="overview-rating-average"]').text
                print (rating) 
            except: 
               print ("none")
        
            try: 
                orders = driver.find_element(By.XPATH,'//span[@class="product-reviewer-sold"]').text
                orderss = orders.replace('orders', '')
                print(orderss)
            except: 
               print ("none")
        
            try: 
                price = driver.find_element(By.XPATH,'//span[@class="uniform-banner-box-price"]').text                                
                pricee = price.replace('MAD', '')
                print(pricee)
            except: 
                try:
                    price = driver.find_element(By.XPATH,'//span[@class="product-price-value"]').text
                    pricee = price.replace('MAD', '')
                    print(pricee)
                except:    
                    print ("none")    

            currency = 'MAD'        
        
            try: 
                ship = driver.find_element(By.XPATH,'//div[@class="dynamic-shipping-line dynamic-shipping-titleLayout"]').text
                print (ship) 
            except: 
                print ("none")        
        
            try: 
                store = driver.find_element(By.XPATH,'//h3[@class="store-name"]').text
                print (store) 
            except: 
                print ("none")  

            try: 
                check = driver.find_element(By.XPATH,'//span[@data-role="positive-feedback"]').text
                leng = len(check)
                check = [x for x in check]
                check = ''.join(check[0:5])
                print(check) 
            except: 
                print ("none")  
        
            try: 
                follow = driver.find_element(By.XPATH,'//p[@class="num-followers"]').text
                followers = follow.replace('Followers', '')
                print(followers)
            except: 
                print ("none")  
                
            try:
                driver.get(iframe)
                try: 
                    feedback = int(''.join(i for i in driver.find_element(By.CSS_SELECTOR,'#transction-feedback > div').text if i.isdigit()))
                    print (feedback) 
                except: 
                    print ("none")
            
                try: 
                    picture = driver.find_element(By.CSS_SELECTOR,'#cb-withPictures-filter +em').text
                    print (picture) 
                except: 
                    print ("none")
            except:    
                print ("none") 

            row = [title, pricee, currency,rating, orderss, ship, store, url, check, followers, feedback, picture]
            results.append(row)   

        df = pd.DataFrame(results , columns=("Title","Price","Currency","Stars","Orders","Shipcost","Supplier","Productlinks","Check","Follow","Feedback", "Picture" ))
            
        data = df.to_dict(orient = 'records')    
    
        collection.insert_many(data)  

   

def bey(dropdown,mylist,subject):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("start-maximized")
    driver = webdriver.Chrome('C:/Users/ADMIN/Desktop/chromedriver.exe',chrome_options=options)
    url1 ='https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText='+subject+'+&ltype=wholesale&SortType=total_tranpro_desc&page={}'

    client = MongoClient("mongodb://localhost:27017/")    
             # use variable db and collection names
    collection_name = subject
    collection = client["db2"][collection_name] 
    x = collection.delete_many({})   
    flg = True   
        
    
    for page_nb in range(1, 2): 
    
        print('---', page_nb, '---') 
    
        driver.get(url1.format(page_nb))

        if flg:
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@style,'display: block')]//img[contains(@src,'TB1')]"))).click()
            except:
                pass
            
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@class='_24EHh']"))).click()
            except:
                pass
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ship-to"))).click()
            
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "country-selector"))).click()
            
            ship_to_australia_element = driver.find_element(By.XPATH, "//li[@class='address-select-item ']//span[@class='shipping-text' and text()='Australia']")
            actions.move_to_element(ship_to_australia_element).perform()
            time.sleep(0.5)
            ship_to_australia_element.click()
            
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-role='save']"))).click()
            
            flg = False

        urls = set()
        results = []
        for i in range(5):
            block = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/item/"]')]
            urls.update(block)
            driver.execute_script("window.scrollBy(0, arguments[0]);", 1200)
            time.sleep(2)
        for url in urls:
        
            driver.get(url)
            current_offset = 0
            while True:
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                sleep(.5)  # JavaScript has time to add elements
                new_offset = driver.execute_script("return window.pageYOffset;")
        
                try:
                        iframe = driver.find_element(By.CSS_SELECTOR, '#feedback iframe').get_attribute('src')
                except:
                        iframe = None
                if new_offset <= current_offset or iframe:
                    break
                current_offset = new_offset
        
            print(url)
            try: 
                title = driver.find_element(By.XPATH,'//h1[@class="product-title-text"]').text
                print (title) 
            except: 
                print ("none")
                
            try: 
                rating = driver.find_element(By.XPATH,'//span[@class="overview-rating-average"]').text
                print (rating) 
            except: 
               print ("none")
        
            try: 
                orders = driver.find_element(By.XPATH,'//span[@class="product-reviewer-sold"]').text
                orderss = orders.replace('orders', '')
                print(orderss)
            except: 
               print ("none")
        
            try: 
                price = driver.find_element(By.XPATH,'//span[@class="uniform-banner-box-price"]').text                                
                pricee = price.replace('MAD', '')
                print(pricee)
            except: 
                try:
                    price = driver.find_element(By.XPATH,'//span[@class="product-price-value"]').text
                    pricee = price.replace('MAD', '')
                    print(pricee)
                except:    
                    print ("none")    

            currency = 'MAD'        
        
            try: 
                ship = driver.find_element(By.XPATH,'//div[@class="dynamic-shipping-line dynamic-shipping-titleLayout"]').text
                print (ship) 
            except: 
                print ("none")        
        
            try: 
                store = driver.find_element(By.XPATH,'//h3[@class="store-name"]').text
                print (store) 
            except: 
                print ("none")  

            try: 
                check = driver.find_element(By.XPATH,'//span[@data-role="positive-feedback"]').text
                leng = len(check)
                check = [x for x in check]
                check = ''.join(check[0:5])
                print(check) 
            except: 
                print ("none")  
        
            try: 
                follow = driver.find_element(By.XPATH,'//p[@class="num-followers"]').text
                followers = follow.replace('Followers', '')
                print(followers)
            except: 
                print ("none")  
                
            try:
                driver.get(iframe)
                try: 
                    feedback = int(''.join(i for i in driver.find_element(By.CSS_SELECTOR,'#transction-feedback > div').text if i.isdigit()))
                    print (feedback) 
                except: 
                    print ("none")
            
                try: 
                    picture = driver.find_element(By.CSS_SELECTOR,'#cb-withPictures-filter +em').text
                    print (picture) 
                except: 
                    print ("none")
            except:    
                print ("none") 

            row = [title, pricee, currency,rating, orderss, ship, store, url, check, followers, feedback, picture]
            results.append(row)   

        df = pd.DataFrame(results , columns=("Title","Price","Currency","Stars","Orders","Shipcost","Supplier","Productlinks","Check","Follow","Feedback", "Picture" ))
            
        data = df.to_dict(orient = 'records')    
    
        collection.insert_many(data)  

def scraping(dropdown,mylist,subject):
    start_time = time.time()
    #options = Options()
    #options.headless = False
    #driver = webdriver.Edge(executable_path=r"C:\Users\ADMIN\Desktop\msedgedriver.exe",options=options)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome('C:/Users/ADMIN/Desktop/chromedriver.exe',chrome_options=options)
    url ='https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText='+subject+'+&ltype=wholesale&SortType=total_tranpro_desc&page={}'
    
    client = MongoClient("mongodb://localhost:27017/")    
         # use variable db and collection names
    collection_name = subject
    collection = client["db2"][collection_name] 
    x = collection.delete_many({})   
    flg = True
    for page_nb in range(1, 2):
        
        print('---', page_nb, '---')    
        wait = WebDriverWait(driver, 10)
        actions = ActionChains(driver)
        driver.get(url.format(page_nb))

        if flg:
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@style,'display: block')]//img[contains(@src,'TB1')]"))).click()
            except:
                pass
            
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@class='_24EHh']"))).click()
            except:
                pass
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ship-to"))).click()
            
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "country-selector"))).click()
            
            ship_to_australia_element = driver.find_element(By.XPATH, "//li[@class='address-select-item ']//span[@class='shipping-text' and text()='Australia']")
            actions.move_to_element(ship_to_australia_element).perform()
            time.sleep(0.5)
            ship_to_australia_element.click()
            
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-role='save']"))).click()
            
            flg = False

        #country_button = driver.find_element_by_class_name('ship-to')
        #country_button.click()
        #country_buttonn = driver.find_element_by_class_name('shipping-text')
        #country_buttonn.click()     
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='address-select-item ']//span[@class='shipping-text' and text()='Spain']"))).click()  
        #country_buttonnn = driver.find_element_by_class_name('ui-button ')
        #country_buttonnn.click() 
        sleep(2)
        current_offset = 0
        while True:
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            sleep(.5)  # JavaScript has time to add elements
            new_offset = driver.execute_script("return window.pageYOffset;")
            if new_offset <= current_offset:
                break
            current_offset = new_offset
        sleep(3)
        tree = html.fromstring(driver.page_source)
        results = []
        for product in tree.xpath('//div[@class="JIIxO"]//a'):
            title = product.xpath('.//h1/text()')
            if title:
                title = title[0]
                price = product.cssselect('div.mGXnE._37W_B span')
                leng = len(price)
                price = [x.text for x in price]
                
                currency = price[0]
                price = ''.join(price[1:])
                stars = product.xpath('.//span[@class="eXPaM"]/text()')
                if stars :
                    stars  = stars [0]
                else:
                    stars  = 'None'
                nb_sold = product.xpath('.//span[@class="_1kNf9"]/text()')
                if nb_sold:
                    nb_sold = nb_sold[0]
                else:
                    nb_sold = 'None'
                supl = product.xpath('.//a[@class="ox0KZ"]/text()')
                if supl:
                    supl = supl[0]
                else:
                    supl = 'None'
                ship_cost = product.xpath('.//span[@class="_2jcMA"]/text()')
                if ship_cost:
                    ship_cost = ship_cost[0]
                else:
                    ship_cost = 'None'
                product_links = product.xpath('./@href')
                if product_links:
                    product_links = str( product_links[0])
                row = [title, price, currency, stars, nb_sold, ship_cost, supl, product_links]
                results.append(row)
        # driver.close()-------Remove this code so driver is open and can open URL
        df = pd.DataFrame(results , columns=("Title","Price", "Currency", "Stars", "Orders", "Shipcost", "Supplier", "Productlinks" ))
        
        data = df.to_dict(orient = 'records')    
        
        collection.insert_many(data)      
     