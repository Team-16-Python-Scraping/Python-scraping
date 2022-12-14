from tkinter import messagebox
from tkinter import ttk
from bs4 import BeautifulSoup
from selenium import webdriver
import webbrowser
import time
import csv
from Product import Product
import tkinter as tk
from tkinter import BOTH, CENTER, END, LEFT, RIGHT, Y, Frame, Label, Listbox, Scrollbar, Toplevel, ttk
import webbrowser
PATH = r'C:\Program Files (x86)\Chromedriver\chromedriver.exe' #link to chromedriver app in your pc

def getPosition(root):
    window_width = 800
    window_height = 500
    # get the screen size of your computer [width and height using the root object as foolows]
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Get the window position from the top dynamically as well as position from left or right as follows
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    return f'{window_width}x{window_height}+{position_right}+{position_top}'
    # this is the line that will center your window


def generateLinks(searched_product):
    urlList = []
    for i in range(1):
        search = searched_product.lower().replace(' ', '%20')
        url = "https://shopee.vn/search?keyword={}&page={}".format(search, i)
        urlList.append(url)
    return urlList


def getHtml(url):  # get source code of web
    driver = webdriver.Chrome(executable_path=PATH)
    driver.get(url)
    driver.execute_script("""
        var scroll = document.body.scrollHeight / 4;
        var i = 0;
        function scrollit(i) {
           window.scrollBy({top: scroll, left: 0, behavior: 'smooth'});
           i++;
           if (i < 30) {
               setTimeout(scrollit, 350, i);
           }
        }
        scrollit(i);
    """)

    # the script above for auto scroll in order to display all items which are written by js
    time.sleep(10)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, 'lxml')
    return soup


productList = []  # use global var for fill the table and export to csv file


def fillProductList(searched_product):
    try:
        global productList
        productList.clear()
        url = generateLinks(searched_product)[0]
        soup = getHtml(url)
        items = soup.find_all('div', class_='col-xs-2-4 shopee-search-item-result__item')

        for item in items:

            # name
            name_item = item.find('div', class_='ie3A+n bM+7UW Cve6sh').text
            price = item.findAll('span', class_='ZEgDH9')

            minPrice, maxPrice = 0, 0
            if len(price) > 1:
                minPrice, maxPrice = [int(x.text.replace('.', '')) for x in price]
            else:
                minPrice = maxPrice = int(price[0].text.replace('.', ''))

            # rating
            stars = item.findAll('div', class_='shopee-rating-stars__lit')
            rating = 0
            if stars != None:
                for star in stars:
                    rating += float(star['style'].split()[1][:-2]) / 100

            quantity, sales = item.find('div', class_='r6HknA uEPGHT'), '0'
            if quantity != None:
                sales = quantity.text.split()[-1].replace(',', '').replace('k', '000')

            # link
            link_item = 'https://shopee.vn' + item.find('a')['href']
            p = Product(name_item, minPrice, maxPrice, rating, sales, link_item)
            productList.append(p)
    except:
        messagebox.showerror("Error", '???? c?? l???i x???y ra!\nVui l??ng th??? l???i')


def writeToFile(name):
    if len(name) == 0:
        messagebox.showerror("Error", "B???n ch??a nh???p t??n file")
    else:
        csvFile = open(f'{name}.csv', 'w+', encoding='utf-16', newline='')
        try:
            writer = csv.writer(csvFile, delimiter='\t')
            writer.writerow(
                ('T??n s???n ph???m', 'Gi?? nh??? nh???t', 'Gi?? l???n nh???t', '????nh gi?? s???n ph???m', 'Doanh s???', 'Link s???n ph???m'))
            writer.writerows(productList)
        except:
            messagebox.showerror('ERROR', '???? c?? l???i x???y ra!')
        finally:
            csvFile.close()
            messagebox.showinfo("Sucessfully!", '???? l??u v??o file th??nh c??ng')

def clearTreeView(productTree):
    for i in productTree.get_children():
            productTree.delete(i)
def fillTreeView(productTree):
    contacts = []
    for i in range(0,len(productList)):
        contacts.append((i+1,productList[i].name,productList[i].minPrice,productList[i].maxPrice,productList[i].sales,'%.1f'%productList[i].rating,productList[i].link))
    productTree.tag_configure('oddrow',background="#7DE5ED")
    productTree.tag_configure('evenrow',background="white")
    count =0
    for contact in contacts:
        if(count%2==0):
            productTree.insert('',tk.END,values=contact,tags="oddrow")
        else:
            productTree.insert('',tk.END,values=contact,tags="evenrow")
        count+=1
def showProducts(): #ProductTable
    table = Toplevel()
    table.geometry("1200x500")
    # Construct Treeview  
    columns = ['S_T_T','T??n_s???n_ph???m','Gi??_nh???_nh???t','Gi??_l???n_nh???t','????_b??n','Sao_????nh_gi??','Link_s???n_ph???m']
    productTree = ttk.Treeview(table,columns = columns,show = 'headings',cursor="hand2 orange")
    def columnConstructor(cl,text,w):
        productTree.heading(cl,text=text)
        productTree.column(cl,width=w,anchor=CENTER)
    columnConstructor('S_T_T','STT',50)
    columnConstructor('T??n_s???n_ph???m','T??n s???n ph???m',210)
    columnConstructor('Gi??_nh???_nh???t','Gi?? nh??? nh???t',100)
    columnConstructor('Gi??_l???n_nh???t','Gi?? l???n nh???t',100)
    columnConstructor('????_b??n','???? b??n',80)
    columnConstructor('Sao_????nh_gi??','Sao ????nh gi??',100)
    columnConstructor('Link_s???n_ph???m','Link s???n ph???m',300)
    fillTreeView(productTree)
    s2= ttk.Style()
    s2.theme_use("default")
    s2.configure('Treeview.Heading',background ="orange",bd =1)
    s2.configure('Treeview',rowheight =40,border =1)
    s2.map('Treeview',background=[('selected','orange')],)
    #Access to link of selected product
    def goLink(event):
        input_id = productTree.selection()
        input_item = productTree.set(input_id,column="Link_s???n_ph???m")
        webbrowser.open('{}'.format(input_item))
    productTree.bind("<Double-1>",goLink)
    productTree.grid(row=0, column=0, sticky='nsew')
    #Scrollbar
    scrollbar = ttk.Scrollbar(table,orient=tk.VERTICAL,command=productTree.yview)
    productTree.configure(yscroll =scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
def showProducts(): #ProductTable
    table = Toplevel()
    table.geometry("1200x424")
    # Construct Treeview  
    columns = ['S_T_T','T??n_s???n_ph???m','Gi??_nh???_nh???t','Gi??_l???n_nh???t','????_b??n','Sao_????nh_gi??','Link_s???n_ph???m']
    productTree = ttk.Treeview(table,columns = columns,show = 'headings',cursor="hand2 orange")
    def columnConstructor(cl,text,w):
        productTree.heading(cl,text=text)
        productTree.column(cl,width=w,anchor=CENTER)
    columnConstructor('S_T_T','STT',50)
    columnConstructor('T??n_s???n_ph???m','T??n s???n ph???m',210)
    columnConstructor('Gi??_nh???_nh???t','Gi?? nh??? nh???t',100)
    columnConstructor('Gi??_l???n_nh???t','Gi?? l???n nh???t',100)
    columnConstructor('????_b??n','???? b??n',80)
    columnConstructor('Sao_????nh_gi??','Sao ????nh gi??',100)
    columnConstructor('Link_s???n_ph???m','Link s???n ph???m',300)
    contacts = []
    for i in range(0,len(productList)):
        contacts.append((i+1,productList[i].name,productList[i].minPrice,productList[i].maxPrice,productList[i].sales,'%.1f'%productList[i].rating,productList[i].link))
    productTree.tag_configure('oddrow',background="#7DE5ED")
    productTree.tag_configure('evenrow',background="white")
    count =0
    for contact in contacts:
        if(count%2==0):
            productTree.insert('',tk.END,values=contact,tags="oddrow")
        else:
            productTree.insert('',tk.END,values=contact,tags="evenrow")
        count+=1
    s2= ttk.Style()
    s2.theme_use("default")
    s2.configure('Treeview.Heading',background ="orange",bd =1)
    s2.configure('Treeview',rowheight =40,border =1)
    s2.map('Treeview',background=[('selected','orange')],)
    #Access to link of selected product
    def goLink(event):
        input_id = productTree.selection()
        input_item = productTree.set(input_id,column="Link_s???n_ph???m")
        webbrowser.open('{}'.format(input_item))
    productTree.bind("<Double-1>",goLink)
    productTree.grid(row=0, column=0, sticky='nsew')
    #Scrollbar
    scrollbar = ttk.Scrollbar(table,orient=tk.VERTICAL,command=productTree.yview)
    productTree.configure(yscroll =scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    def sortByPrice():
        clearTreeView(productTree)
        productList.sort(key= lambda x : (x.minPrice, x.maxPrice))
        fillTreeView(productTree)
    def sortByRating():
        clearTreeView(productTree)
        productList.sort(key= lambda x : -x.rating)
        fillTreeView(productTree)
    def sortBySales():
        clearTreeView(productTree)
        productList.sort(key= lambda x : -int(x.sales))
        fillTreeView(productTree)

    def sortByPrice():
        clearTreeView(productTree)
        productList.sort(key= lambda x : (x.minPrice, x.maxPrice))
        fillTreeView(productTree)
    def sortByRating():
        clearTreeView(productTree)
        productList.sort(key= lambda x : -x.rating)
        fillTreeView(productTree)
    def sortBySales():
        clearTreeView(productTree)
        productList.sort(key= lambda x : -int(x.sales))
        fillTreeView(productTree)

    #Set Selections
    selections = tk.Frame(table,relief="solid")
    selections.place(x=980,y=60,height= 350,width=200)
    btn_sortPrice = tk.Button(selections,text="S???p x???p theo gi?? t??ng d???n",pady=10,fg="white",bg="black",cursor="hand2", command=sortByPrice)
    btn_sortPriceReverse = tk.Button(selections,text="S???p x???p theo doanh s??? gi???m d???n",pady=10,fg="white",bg="black",cursor="hand2", command=sortBySales)
    btn_sortRate = tk.Button(selections,text="S???p x???p theo ????nh gi?? gi???m d???n",pady=10,fg="white",bg="black",cursor="hand2", command=sortByRating)
    lb_exportToFile = tk.Label(selections, text='Nh???p t??n file: ')
    e_exportToFile = tk.Entry(selections, width=40)
    btn_exportToFile = tk.Button(selections, text='L??u v??o file csv!', pady=10, fg='white', bg='green', command=lambda: writeToFile(e_exportToFile.get()))
    btn_sortPrice.pack(pady=10)
    btn_sortPriceReverse.pack(pady=10) 
    btn_sortRate.pack(pady=10) 
    lb_exportToFile.pack(pady=10)
    e_exportToFile.pack(pady=5)
    btn_exportToFile.pack(pady=10)
def accessToShopee(searched_product):
    if len(searched_product) == 0:
        messagebox.showerror("Warning", "B???n ch??a nh???p t??n s???n ph???m")
    else:
        fillProductList(searched_product)
        showProducts()
    
