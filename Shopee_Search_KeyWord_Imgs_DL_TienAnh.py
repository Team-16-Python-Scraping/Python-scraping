import requests
import os
from tqdm import tqdm #thư viện hiện tiến trình tải
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import selenium
from selenium import webdriver
import time

driver = webdriver.Firefox()

def is_valid(url):  # check valid url
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_url(url):
    urls = []
    time.sleep(5)
    for i in range(10):
        driver.execute_script("window.scrollBy(0, 350)")
        time.sleep(1)
    content = driver.page_source
    soup = bs(content, 'html.parser')
    
    for item in soup.select('div[data-sqe="item"]'):
        dataImg = item.img
        if dataImg is not None:
            urls.append(dataImg['src'])
    return urls
        

'''def get_all_images(url):    # lấy url ảnh
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url: # không có url src thì skip
            continue
        img_url = urljoin(url, img_url) # kết hợp https:// với url vừa lấy được tạo thành 1 url hoàn chỉnh
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url): # gọi is_valid
            urls.append(img_url)
    return urls'''


def download(url, pathname):    #tải file ảnh với url vừa lấy được và đặt vào thư mục tự đặt tên
    if not os.path.isdir(pathname): # nếu không có directory của folder thì tạo
        os.makedirs(pathname)
    response = requests.get(url, stream=True)   # tải lần lượt theo từng url
    file_size = int(response.headers.get("Content-Length", 0))  # lấy dung lượng ảnh
    filename = os.path.join(pathname, url.split("/")[-1])   # lấy tên file ảnh
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024) # thanh tiến độ tải, chuyển về bytes thay vì iteration (mặc định trong thư viện tqdm)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)   # chuyền dữ liệu đọc được vào file
            progress.update(len(data))  # cập nhật tiến độ tải


def main(url, path):
    imgs = get_url(url)  # lấy url ảnh
    for img in imgs:
        download(img, path) # tải ảnh với mỗi url


main(driver.get('https://shopee.com/search?keyword=laptop'), 'imgs')