from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
PATH = r'C:\Program Files (x86)\Chromedriver\chromedriver.exe' #link to chromedriver app in your pc


class Product:
    '''
        
    '''
    def __init__(self, name, minPrice, maxPrice, rating, sales, link):
        self.name = name
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        self.rating = rating
        self.sales = sales
        self.link = link
    def __str__(self): # to string method
        return f'{self.name}\t{self.minPrice}\t{self.maxPrice}\t{"%.1f"%self.rating},{self.sales}\t{self.link}'
    def __iter__(self): # for export to csv file
        return iter([self.name, self.minPrice, self.maxPrice, "%.1f"%self.rating, self.sales, self.link])

def generateLinks(searched_product):
    urlList = []
    for i in range(1):
        search = searched_product.lower().replace(' ', '%20')
        url = "https://shopee.vn/search?keyword={}&page={}".format(search, i)
        urlList.append(url)
    return urlList

def getHtml(url): # get source code of web
    driver = webdriver.Chrome(executable_path=PATH)
    driver.get(url)
    # WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'shopee-search-item-result')))
    driver.execute_script("""
    var scroll = document.body.scrollHeight/2;
    var i = 0;
    function scrollit(i) {
        window.scrollBy({top: scroll, left: 0, behavior: 'smooth'});
        i++;
        if (i < 15) {
            setTimeout(scrollit, 300, i);
        }
    }
    scrollit(i);
    """)
    # the script above for auto scroll in order to display all items which are written by js
    time.sleep(8)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, 'lxml')
    return soup

productList = [] # use global var for fill the table and export to csv file

def fillProductList(searched_product):
    global productList
    productList.clear()
    url = generateLinks(searched_product)[0]
    soup = getHtml(url)
    items = soup.find_all('div', class_ = 'col-xs-2-4 shopee-search-item-result__item')
    
    for item in items:
        
        # name
        name_item = item.find('div', class_ = 'ie3A+n bM+7UW Cve6sh').text
        price = item.findAll('span', class_ = 'ZEgDH9')
        
        minPrice, maxPrice = 0, 0
        if len(price) > 1:
            minPrice, maxPrice = [int(x.text.replace('.', '')) for x in price]
        else:
            minPrice = maxPrice = int(price[0].text.replace('.', ''))

        # rating
        stars = item.findAll('div', class_ = 'shopee-rating-stars__lit')
        rating = 0
        if stars != None:
            for star in stars:
                rating += float(star['style'].split()[1][:-2])/100

        quantity, sales = item.find('div', class_ = 'r6HknA uEPGHT'), '0'
        if quantity != None:
            sales = quantity.text.split()[-1].replace(',', '').replace('k', '000')

        #link
        link_item = 'https://shopee.vn' + item.find('a')['href']
        p = Product(name_item, minPrice, maxPrice, rating, sales, link_item)
        productList.append(p)

def writeToFile(name, searched_product):
    if len(productList) == 0:
        fillProductList(searched_product)
    csvFile = open(f'{name}.csv', 'w+', encoding= 'utf-16', newline='')
    try:
        writer = csv.writer(csvFile, delimiter = '\t')
        writer.writerow(('Tên sản phẩm', 'Giá nhỏ nhất', 'Giá lớn nhất', 'Đánh giá sản phẩm', 'Doanh số', 'Link sản phẩm'))
        writer.writerows(productList)
    finally:
        csvFile.close()

def accessToShopee(myList, searched_product):
    fillProductList(searched_product)
    for product in productList:
        myList.insert(END, product.__str__())
        # print(product)
    
    
