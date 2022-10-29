import urllib
from urllib.request import *
from bs4 import BeautifulSoup

url = input("Nhap 1 link bai bao cu the\n")

html  = urlopen(url)#co trong urllib.request
bsObj = BeautifulSoup(html, "html.parser")
imgs = bsObj.findAll("img")#tim trong tag <img> cua html
for img in imgs:
    src = img['src'] #lay attribute 'src'
    if src == "None":
      continue
    print(src)
