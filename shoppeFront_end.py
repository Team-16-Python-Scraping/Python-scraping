from msilib.schema import ListBox
import tkinter as tk
from tkinter import BOTH, CENTER, END, LEFT, RIGHT, Y, Frame, Label, Listbox, Scrollbar, Toplevel, ttk
from tkinter import font
from tkinter import messagebox
import webbrowser
from PIL import Image, ImageTk

class Product:
    def __init__(self, name, minPrice, maxPrice, rating, sales, link):
        self.name = name
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        self.rating = rating
        self.sales = sales
        self.link = link
    def __str__(self):
        return f'{self.name}\t{self.minPrice}\t{self.maxPrice}\t{"%.1f"%self.rating},{self.sales}\t{self.link}'
    def __iter__(self):
        return iter([self.name, self.minPrice, self.maxPrice, "%.1f"%self.rating, self.sales, self.link])
def getPosition(root):
    window_width = 800
    window_height = 500
    # get the screen size of your computer [width and height using the root object as foolows]
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Get the window position from the top dynamically as well as position from left or right as follows
    position_top = int(screen_height/2 -window_height/2)
    position_right = int(screen_width / 2 - window_width/2)
    return f'{window_width}x{window_height}+{position_right}+{position_top}'
    # this is the line that will center your window


def mainDisplay():
    # intro()
    root = tk.Tk()
    root.title('TEAM 16 - Python scraping')
    root.geometry(getPosition(root))
    labelWidth = 800
    labelHeight = 500
    maxsize = (labelWidth, labelHeight)
    img = Image.open("r.jpg")
    img = img.resize(maxsize)
    bg = ImageTk.PhotoImage(img)
    rootImg = tk.Label(root, image=bg)
    rootImg.place(in_=root, x=0, y=0)

    btn_aboutUs = tk.Label(root, text='ABOUT US', bg='black',
                           fg='white', width=9, height=2,
                           font=('Inter', 10, 'bold'))
    btn_aboutUs.pack(pady=2, anchor='e')

    style = ttk.Style()
    style.theme_create("Tab", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 4], "background": '#d2ffd2'},
            "map": {"background": [("selected", '#FF8C00')],
                    "expand": [("selected", [1, 1, 1, 0])]}}})
    style.theme_use("Tab")

    myfont = ('Inter', '11', 'bold')

    tabControl = ttk.Notebook(root)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    s = ttk.Style()
    s.configure('TNotebook.Tab', font= myfont)

    tabControl.add(tab1, text='Get product from shopee')
    tabControl.add(tab2, text='Get image from URL', )
    tabControl.pack(expand=1, fill="both")

    ttk.Label(tab1) # root for shopee
    lbSearch = tk.Label(tab1, text='Nhập tên sản phẩm: ', font=myfont)
    eSearch = tk.Entry(tab1, width=72, font=myfont)
    frame = tk.LabelFrame(tab1, text='Danh sách thuộc tính cần lấy về', width=500, height=200)

    lbSearch.place(x=10, y=10)
    eSearch.place(x=180, y=10)
    frame.place(x=10, y=50)

    checkVar = tk.IntVar(value=1)
    ckbName = ttk.Checkbutton(frame, text='Tên sản phẩm', state=tk.DISABLED, variable=checkVar)
    ckbMinPrice = ttk.Checkbutton(frame, text='Giá nhỏ nhất', state=tk.DISABLED, variable=checkVar)
    ckbMaxPrice = ttk.Checkbutton(frame, text='Giá lớn nhất', state=tk.DISABLED, variable=checkVar)
    ckbRating = ttk.Checkbutton(frame, text='Đánh giá (sao)', state=tk.DISABLED, variable=checkVar)
    ckbLink = ttk.Checkbutton(frame, text='Link sản phẩm', state=tk.DISABLED, variable=checkVar)

    ckbName.place(x=15, y=10)
    ckbMinPrice.place(x=15, y=45)
    ckbMaxPrice.place(x=15, y=80)
    ckbRating.place(x=15, y=115)
    ckbLink.place(x=15, y=150)

    lbNumberOfPage = tk.Label(tab1, text='Số trang muốn lấy dữ liệu: ')
    eNumberofPage = tk.Entry(tab1, width=20, textvariable=checkVar, state="readonly")
    lbNumberOfPage.place(x=10, y=265)
    eNumberofPage.place(x=170, y=265)

    imgLogo = ImageTk.PhotoImage(Image.open("logoshoppe.png").resize((205, 205)))
    lbLogo = tk.Label(tab1, image=imgLogo)

    lbLogo.place(x=550, y=45)
    def showProducts(s): #ProductTable
        if s=="": messagebox.showerror("Warning","Bạn chưa nhập tên sản phẩm")
        else :
            productList = [
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com"),
                Product("Hung",1500,2000,5,2000,"google.com")
            ]
            table = Toplevel()
            table.geometry("1200x424")
            # Construct Treeview  
            columns = ('S_T_T','Tên_sản_phẩm','Giá_nhỏ_nhất','Giá_lớn_nhất','Đã_bán','Sao_đánh_giá','Link_sản_phẩm')
            productTree = ttk.Treeview(table,columns = columns,show = 'headings',cursor="hand2 orange")
            productTree.heading('S_T_T',text='STT')
            productTree.column('S_T_T',width=50,anchor=CENTER)
            productTree.heading('Tên_sản_phẩm',text='Tên sản phẩm')
            productTree.column('Tên_sản_phẩm',anchor=CENTER)
            productTree.heading('Giá_nhỏ_nhất',text='Giá nhỏ nhất')
            productTree.column('Giá_nhỏ_nhất',width=100,anchor=CENTER)
            productTree.heading('Giá_lớn_nhất',text='Giá lớn nhất')
            productTree.column('Giá_lớn_nhất',width=100,anchor=CENTER)
            productTree.heading('Đã_bán',text='Đã bán')
            productTree.column('Đã_bán',width=80,anchor=CENTER)
            productTree.heading('Sao_đánh_giá',text='Sao đánh giá')
            productTree.column('Sao_đánh_giá',width=100,anchor=CENTER)
            productTree.heading('Link_sản_phẩm',text='Link sản phẩm')
            productTree.column('Link_sản_phẩm',anchor=CENTER,width=300)
            contacts = []
            for i in range(0,len(productList)):
                contacts.append((i+1,productList[i].name,productList[i].minPrice,productList[i].maxPrice,productList[i].sales,productList[i].rating,productList[i].link))
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
                input_item = productTree.set(input_id,column="Link_sản_phẩm")
                webbrowser.open('{}'.format(input_item))
            productTree.bind("<Double-1>",goLink)
            productTree.grid(row=0, column=0, sticky='nsew')
            #Scrollbar
            scrollbar = ttk.Scrollbar(table,orient=tk.VERTICAL,command=productTree.yview)
            productTree.configure(yscroll =scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')

            #Set Selections
            selections = tk.Frame(table,relief="solid")
            selections.place(x=980,y=60,height= 285,width=200)
            btn_sortPrice = tk.Button(selections,text="Sắp xếp theo giá tăng dần",pady=10,fg="white",bg="black",cursor="hand2")
            btn_sortPriceReverse = tk.Button(selections,text="Sắp xếp theo giá giảm dần",pady=10,fg="white",bg="black",cursor="hand2")
            btn_sortRate = tk.Button(selections,text="Sắp xếp theo rate giảm dần",pady=10,fg="white",bg="black",cursor="hand2" )
            btn_sortName = tk.Button(selections,text="Sắp xếp theo tên sản phẩm",pady=10,fg="white",bg="black",cursor="hand2")
            btn_sortPrice.pack(pady=10)
            btn_sortPriceReverse.pack(pady=10) 
            btn_sortRate.pack(pady=10) 
            btn_sortName.pack(pady=10)

    btnSearch = tk.Button(tab1, text='TRA CỨU!', font=myfont,command= lambda :  showProducts(eSearch.get()))
    lbCopyRight = tk.Label(tab1, text='@2022 - team 16 PTIT',
                           height=2, bg='black', fg='white',
                           font=myfont, relief=tk.SUNKEN, width=root.winfo_screenwidth(), anchor=tk.W)

    btnSearch.place(x=550, y=270)
    lbCopyRight.pack(side='bottom', fill='y')
    # Root for Image
    ttk.Label(tab2)
    lbSearch = tk.Label(tab2, text='Nhập link ảnh : ', font=myfont)
    eSearch2 = tk.Entry(tab2, width=60, font=myfont)
    btnSearch = tk.Button(tab2, text="Tìm ngay",font=myfont)

    lbSearch.place(x=10, y=10)
    eSearch2.place(x=145, y=10)
    btnSearch.place(x=660,y=5)

    lbCopyRight = tk.Label(tab2, text='@2022 - team 16 PTIT',
                           height=2, bg='black', fg='white',
                           font=myfont, relief=tk.SUNKEN, width=root.winfo_screenwidth(), anchor=tk.W)
    lbCopyRight.pack(side='bottom', fill='y')
    root.mainloop()

mainDisplay()