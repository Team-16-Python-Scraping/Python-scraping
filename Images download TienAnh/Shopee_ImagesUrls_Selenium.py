from bs4 import BeautifulSoup
from selenium import webdriver
import time
   
driver =webdriver.Firefox()

images=[]

driver.get('https://shopee.com/search?keyword=laptop')

time.sleep(5)
for i in range(10):
    driver.execute_script("window.scrollBy(0, 350)")
    time.sleep(1)
    
content=driver.page_source
soup=BeautifulSoup(content, 'html.parser')

for item in soup.select('div[data-sqe="item"]'):
    dataImg=item.img
    
    if dataImg is not None:
        images.append(dataImg['src'])
print(images)