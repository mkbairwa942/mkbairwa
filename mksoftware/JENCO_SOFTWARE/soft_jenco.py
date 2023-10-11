# from copy import copy
# import numpy as np
# from sqlalchemy import create_engine
# import urllib
# import itertools
# import pprint
# import pandas as pd
# from datetime import date
# import xlwings as xw
# import os

from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import random,os
from tkinter import messagebox
import tempfile
from time import strftime


class Bill_App:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1360x800+0+0")
        self.root.title("Accounting Software")

        #Menu
        menubar = Menu(self.root)

        #file menu
        Accounts=Menu(menubar,tearoff=0)
        Accounts.add_command(label="Account",command=self.open_win)
        Accounts.add_command(label="Agent")
        Accounts.add_command(label="City")
        Accounts.add_command(label="Transport")
        Accounts.add_command(label="Haste")
        Accounts.add_command(label="Quality")
        Accounts.add_command(label="Company")
        Accounts.add_separator()
        Accounts.add_command(label="Exit",command=root.quit)
        menubar.add_cascade(label="Accounts",menu = Accounts)

        #Edit Menu
        #file menu
        Transection=Menu(menubar,tearoff=0)
        Transection.add_command(label="Purchase")
        Transection.add_command(label="Delivery Challan")
        Transection.add_command(label="Sales Bill")
        Transection.add_command(label="Debit Note")
        Transection.add_command(label="Creadit Note")
        Transection.add_command(label="Bank")
        Transection.add_command(label="Account Entry")
        Transection.add_command(label="Grey")
        Transection.add_command(label="Packing Slip/Loose Stock")
        Transection.add_command(label="Bill Adjustment")
        Transection.add_command(label="Gate Pass")
        Transection.add_command(label="SMS / Message Process")
        Transection.add_command(label="Delivery Slip Print")
        menubar.add_cascade(label="Transection",menu = Transection)

        #Report
        Reports=Menu(menubar,tearoff=0)
        Reports.add_command(label="E-Invoice Sales")
        Reports.add_command(label="E-Invoice Credit Note")
        Reports.add_command(label="Invoice Print / Bill Print")
        Reports.add_command(label="General Purcahse")
        Reports.add_command(label="Grey Purchase")
        Reports.add_command(label="Sales Ankada")
        Reports.add_command(label="Sales Report")
        Reports.add_command(label="Bank / Cash Book")
        Reports.add_command(label="Statment")
        Reports.add_command(label="Ledger")
        Reports.add_command(label="Final Account Report")
        Reports.add_command(label="Grey Fabric Account")
        Reports.add_command(label="Stock report")
        Reports.add_command(label="Packing Report / Bales Stock")
        Reports.add_command(label="Gate Pass / Delivery Challan")
        Reports.add_command(label="Sales Bill Outstanding")
        Reports.add_command(label="Purchase Bills Outstanding")
        Reports.add_command(label="Ledger")
        Reports.add_command(label="Final Account Report")
        Reports.add_command(label="Grey Fabric Account")
        Reports.add_command(label="Merge Report")
        Reports.add_command(label="Statment (New)")
        Reports.add_command(label="Stock View")
        Reports.add_command(label="GST Reports")
        menubar.add_cascade(label="Reports",menu = Reports)

        #USE Full
        Usefull=Menu(menubar,tearoff=0)
        Usefull.add_command(label="Company & Year Selection")
        Usefull.add_command(label="Password Change")
        Usefull.add_command(label="Updation")
        Usefull.add_command(label="Previous Year")
        Usefull.add_command(label="Master Reports")
        Usefull.add_command(label="Calcultor")
        Usefull.add_command(label="Sales Report")
        Usefull.add_command(label="Stocker Master")
        Usefull.add_command(label="Mail Report")
        menubar.add_cascade(label="Usefull",menu = Usefull)

        #Exit
        Exit=Menu(menubar,tearoff=0)
        Exit.add_command(label="Exit",command=root.quit)
        menubar.add_cascade(label="Exit",menu = Exit)

        root.config(menu=menubar)

        main_frame = ttk.Frame(root)

        account_page= ttk.Frame(main_frame)
        account_page_lb=ttk.Label(account_page,text="Account Master",font=("Bold",20))
        account_page_lb.pack(pady=100)
        
        agent_page= ttk.Frame(main_frame)
        agent_page_lb=ttk.Label(agent_page,text="Agent Master",font=("Bold",20))
        agent_page_lb.pack(pady=100)
        
        city_page= ttk.Frame(main_frame)
        city_page_lb=ttk.Label(city_page,text="City Master",font=("Bold",20))
        city_page_lb.pack(pady=100)
        
        transport_page= ttk.Frame(main_frame)
        transport_page_lb=ttk.Label(transport_page,text="Transport Master",font=("Bold",20))
        transport_page_lb.pack(pady=100)

        self.pages=[account_page,agent_page,city_page,transport_page]
        self.count = 0

    def open_win(self):
        if not self.count>len(self.pages)-2:
            for p in self.pages:
                p.pack_forget()
            self.count +=1
            page=self.pages[self.count]
            page.pack(pady=100)

if __name__== '__main__':
    root=Tk()
    obj=Bill_App(root)
    root.mainloop()


# class Bill_App:
#     def __init__(self,root):
#         self.root=root
#         self.root.geometry("1360x800+0+0")
#         self.root.title("Billing Software")

#         #Variables
#         self.c_name=StringVar()
#         self.c_phone=StringVar()
#         self.bill_no=StringVar()
#         z=random.randint(1000,9999)
#         self.bill_no.set(z)
#         self.c_email=StringVar()
#         self.search_bill=StringVar()
#         self.product=StringVar()
#         self.prices=IntVar()
#         self.qty=IntVar()
#         self.sub_total=StringVar()
#         self.tax_input=StringVar()
#         self.total=StringVar()



#         #Product Categories
#         self.Category=["Select Option","Clothing","LifeStyle","Mobiles"]
#         self.SubCatClothing=["Pant","T-Shirt","Shirt"]
#         self.pant=["Levis","Mufti","Spykar"]
#         self.price_levis=5000
#         self.price_mufti=700
#         self.price_spykar=8000

#         self.t_shirt=["Polo","Roadstar","Jack&Jones"]
#         self.price_polo=1500
#         self.price_roadstar=1800
#         self.price_JackJones=1700

#         self.Shirt=["Peter England","Louis","Park Acenue"]
#         self.price_PeterEngland=2100
#         self.price_Louis=2700
#         self.price_Park=1740

#         self.SubCatLifeSyyle=["Bath Soap","Face Cream","Hair Oil"]
#         self.Bath_soap=["Life Boy","Lux","Santoor","Pearl"]
#         self.price_lifeboy=20
#         self.price_lux=25
#         self.price_santoor=30
#         self.price_pearl=50

#         self.Face_cream=["Ponds","Borolin","Herbel"]
#         self.price_pond=50
#         self.price_borolin=30
#         self.price_herbel=90     

#         self.hairoil=["Aavla","Coconut","Sikakai"]
#         self.price_avala=50
#         self.price_coconut=60
#         self.price_sikakai=70

#         self.SubCatMobile=["Iphone","Samsung","Xiome"]
#         self.Iphoe=["Iphone10","Iphone11","Iphone12"]
#         self.price_Iphone10=50000
#         self.price_Iphone11=60000
#         self.price_Iphone12=70000

#         self.samsung=["SamsungA1","SamsungB12","SamsungC3"]
#         self.price_samsungA1=40000
#         self.price_samsungB12=16000
#         self.price_samsungC3=26000

#         self.xiome=["Xiome45","Xiome90","XiomeNote"]
#         self.price_xiome45= 27000
#         self.price_xiome90=35000
#         self.price_xiomeNote=60000

#         # Image1
#         img1=Image.open("D:\STOCK\Capital_vercel1\mksoftware\image/image1.jpg")
#         img1=img1.resize((850,130),Image.Resampling.HAMMING)
#         self.photoimg1=ImageTk.PhotoImage(img1)

#         lbl_img1=Label(self.root,image=self.photoimg1)
#         lbl_img1.place(x=0,y=0,width=850,height=130)

#         # Image3
#         img2=Image.open("D:\STOCK\Capital_vercel1\mksoftware\image/image5.jpg")
#         img2=img2.resize((850,130),Image.Resampling.HAMMING)
#         self.photoimg2=ImageTk.PhotoImage(img2)

#         # Heading
#         lbl_img2=Label(self.root,image=self.photoimg2)
#         lbl_img2.place(x=500,y=0,width=850,height=130)

#         lbl_title=Label(self.root,text="BILLING SOFTWARE USING PYTHON",font=("times new roman",35,"bold"),bg="white",fg="red")
#         lbl_title.place(x=0,y=130,width=1360,height=45)

#                 #time
#         def time():
#             string=strftime('%H:%M:%S %p')
#             lbl.config(text=string)
#             lbl.after(1000,time)

#         lbl=Label(lbl_title,font=("arial",15,"bold"),fg="blue",bg="white")
#         lbl.place(x=5,y=0,width=120,height=50)
#         time()

#         # Main_Frame
#         Main_Frame=Frame(self.root,bd=5,relief=GROOVE,bg="white")
#         Main_Frame.place(x=0,y=175,width=1360,height=520)
        
#         # Customer_Frame
#         Cust_Frame=LabelFrame(Main_Frame,text="Customer",font=("times new roman",12,"bold"),bg="white",fg="red")
#         Cust_Frame.place(x=10,y=5,width=300,height=140)

#         # Custome_frame_Deatils
#         self.lbl_mob=Label(Cust_Frame,font=("arial",11,"bold"),bg="white",text="Mobile No",bd=4)
#         self.lbl_mob.grid(row=0,column=0,sticky=W,padx=8,pady=5)

#         self.entry_mob=ttk.Entry(Cust_Frame,textvariable=self.c_phone,font=("arial",10,"bold"),width=18)
#         self.entry_mob.grid(row=0,column=1,sticky=W,padx=8,pady=5)

#         self.lbl_name=Label(Cust_Frame,font=("arial",11,"bold"),bg="white",text="Customer Name",bd=4)
#         self.lbl_name.grid(row=1,column=0,sticky=W,padx=8,pady=5)

#         self.entry_name=ttk.Entry(Cust_Frame,textvariable=self.c_name,font=("arial",10,"bold"),width=18)
#         self.entry_name.grid(row=1,column=1,sticky=W,padx=8,pady=5)

#         self.lbl_email=Label(Cust_Frame,font=("arial",11,"bold"),bg="white",text="Customer Email",bd=4)
#         self.lbl_email.grid(row=2,column=0,sticky=W,padx=8,pady=5)

#         self.entry_email=ttk.Entry(Cust_Frame,textvariable=self.c_email,font=("arial",10,"bold"),width=18)
#         self.entry_email.grid(row=2,column=1,sticky=W,padx=8,pady=5)

#         # Product Label_Frame
#         Prod_Frame=LabelFrame(Main_Frame,text="Product",font=("times new roman",12,"bold"),bg="white",fg="red")
#         Prod_Frame.place(x=320,y=5,width=540,height=140)

#         # Category
#         self.lblCategory=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Select Categories",bd=4)
#         self.lblCategory.grid(row=0,column=0,sticky=W,padx=8,pady=5)

#         self.Combo_Category=ttk.Combobox(Prod_Frame,values=self.Category,font=("arial",10,"bold"),width=18,state="readonly")
#         self.Combo_Category.current(0)
#         self.Combo_Category.grid(row=0,column=1,sticky=W,padx=8,pady=5,)
#         self.Combo_Category.bind("<<ComboboxSelected>>",self.Categories)

#         # SubCategory
#         self.lblSubCategory=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Subcategory",bd=4)
#         self.lblSubCategory.grid(row=1,column=0,sticky=W,padx=8,pady=5)

#         self.ComboSubCategory=ttk.Combobox(Prod_Frame,values=[""],font=("arial",10,"bold"),width=18,state="readonly")
#         self.ComboSubCategory.grid(row=1,column=1,sticky=W,padx=8,pady=5)
#         self.ComboSubCategory.bind("<<ComboboxSelected>>",self.Product_add)

#         # Product Name
#         self.lblproduct=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Product Name",bd=4)
#         self.lblproduct.grid(row=2,column=0,sticky=W,padx=8,pady=5)

#         self.ComboProduct=ttk.Combobox(Prod_Frame,textvariable=self.product,font=("arial",10,"bold"),width=18,state="readonly")
#         self.ComboProduct.grid(row=2,column=1,sticky=W,padx=8,pady=5)
#         self.ComboProduct.bind("<<ComboboxSelected>>",self.pricess)

#         # Price
#         self.lblPrice=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Price",bd=4)
#         self.lblPrice.grid(row=0,column=2,sticky=W,padx=8,pady=5)

#         self.ComboPrice=ttk.Combobox(Prod_Frame,textvariable=self.prices,font=("arial",10,"bold"),width=18,state="readonly")
#         self.ComboPrice.grid(row=0,column=3,sticky=W,padx=8,pady=5)

#         # Quantity
#         self.lblQty=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Qty",bd=4)
#         self.lblQty.grid(row=1,column=2,sticky=W,padx=8,pady=5)

#         self.ComboQty=ttk.Entry(Prod_Frame,textvariable=self.qty,font=("arial",10,"bold"),width=20)
#         self.ComboQty.grid(row=1,column=3,sticky=W,padx=8,pady=5)

#         #Middle Frame
#         Middle_Frame=Frame(Main_Frame,bd=10,bg="white")
#         Middle_Frame.place(x=10,y=150,width=848,height=240)

#         imgMiddle1=Image.open("D:\STOCK\Capital_vercel1\mksoftware\image/image1.jpg")
#         imgMiddle1=imgMiddle1.resize((426,250),Image.Resampling.HAMMING)
#         self.photoimg3=ImageTk.PhotoImage(imgMiddle1)

#         lbl_img1=Label(Middle_Frame,image=self.photoimg3)
#         lbl_img1.place(x=0,y=0,width=426,height=250)

#         imgMiddle2=Image.open("D:\STOCK\Capital_vercel1\mksoftware\image/image5.jpg")
#         imgMiddle2=imgMiddle2.resize((426,250),Image.Resampling.HAMMING)
#         self.photoimg4=ImageTk.PhotoImage(imgMiddle2)

#         lbl_img2=Label(Middle_Frame,image=self.photoimg4)
#         lbl_img2.place(x=400,y=0,width=426,height=250)

#         # Search Area
#         Search_Frame=Frame(Main_Frame,bd=2,bg="white")
#         Search_Frame.place(x=870,y=10,width=500,height=35)

#         self.lblBill=Label(Search_Frame,font=("arial",10,"bold"),fg="white",bg="red",text="Bill Number")
#         self.lblBill.grid(row=0,column=0,sticky=W,padx=4,pady=4)
        
#         self.entry_Search=ttk.Entry(Search_Frame,textvariable=self.search_bill,font=("arial",10,"bold"),width=24)
#         self.entry_Search.grid(row=0,column=1,sticky=W,padx=2)
        
#         self.BtnSearch=Button(Search_Frame,command=self.find_bill,width=15,text="Search",font=('arial',10,'bold'),bg="orangered",fg="white",cursor="hand2")
#         self.BtnSearch.grid(row=0,column=2,sticky=W,padx=7)

#         # Right frame Bill Area
#         RightLabelFrame=LabelFrame(Main_Frame,text="Bill Area",font=("times new roman",12,"bold"),bg="white",fg="red")
#         RightLabelFrame.place(x=870,y=45,width=470,height=350)

#         scroll_y=Scrollbar(RightLabelFrame,orient=VERTICAL)
#         self.textarea=Text(RightLabelFrame,yscrollcommand=scroll_y.set,bg="white",fg="blue",font=("times new roman",12,"bold"))
#         scroll_y.pack(side=RIGHT,fill=Y)
#         scroll_y.config(command=self.textarea.yview)
#         self.textarea.pack(fill=BOTH,expand=1)

#         # Bill Counter Label_Frame
#         Bottom_Frame=LabelFrame(Main_Frame,text="Bill Counter",font=("times new roman",12,"bold"),bg="white",fg="red")
#         Bottom_Frame.place(x=0,y=395,width=1345,height=115)

        
#         # Sub Total
#         self.lblSubTotal=Label(Bottom_Frame,font=("arial",10,"bold"),bg="white",text="Sub Total",bd=4)
#         self.lblSubTotal.grid(row=0,column=0,sticky=W,padx=5,pady=2)

#         self.EntrySubTotal=ttk.Entry(Bottom_Frame,textvariable=self.sub_total,font=("arial",10,"bold"),width=20)
#         self.EntrySubTotal.grid(row=0,column=1,sticky=W,padx=5,pady=2)

#         # Taxes
#         self.lblTax=Label(Bottom_Frame,font=("arial",10,"bold"),bg="white",text="GST",bd=4)
#         self.lblTax.grid(row=1,column=0,sticky=W,padx=5,pady=2)

#         self.EntryTax=ttk.Entry(Bottom_Frame,textvariable=self.tax_input,font=("arial",10,"bold"),width=20)
#         self.EntryTax.grid(row=1,column=1,sticky=W,padx=5,pady=2)

#         # Amount
#         self.lblAmount=Label(Bottom_Frame,font=("arial",10,"bold"),bg="white",text="Net Amount",bd=4)
#         self.lblAmount.grid(row=2,column=0,sticky=W,padx=5,pady=2)

#         self.EntryAmount=ttk.Entry(Bottom_Frame,textvariable=self.total,font=("arial",10,"bold"),width=20)
#         self.EntryAmount.grid(row=2,column=1,sticky=W,padx=5,pady=2)

#         # Button Frame
#         Btn_Frame=Frame(Bottom_Frame,bd=2,bg="white")
#         Btn_Frame.place(x=260,y=0)

#         self.BtnAddToCart=Button(Btn_Frame,command=self.AddItem,height=2,width=14,text="Add to Cart",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
#         self.BtnAddToCart.grid(row=0,column=0)

#         self.BtnGenBill=Button(Btn_Frame,command=self.gen_bill,height=2,width=14,text="Generate Bill",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
#         self.BtnGenBill.grid(row=0,column=1)

#         self.BtnSaveBill=Button(Btn_Frame,command=self.save_bill,height=2,width=14,text="Save Bill",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
#         self.BtnSaveBill.grid(row=0,column=2)

#         self.BtnPrint=Button(Btn_Frame,height=2,command=self.iprint,width=14,text="Print",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
#         self.BtnPrint.grid(row=0,column=3)

#         self.BtnClear=Button(Btn_Frame,command=self.clear,height=2,width=14,text="Clear",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
#         self.BtnClear.grid(row=0,column=4)

#         self.BtnExit=Button(Btn_Frame,command=self.root.destroy,height=2,width=14,text="Exit",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
#         self.BtnExit.grid(row=0,column=5)
#         self.welcome()
#     # ===function Declaration====

#     def welcome(self):
#         self.textarea.delete(1.0,END)
#         self.textarea.insert(END,"\t Welcome Codewith Mukesh Mini Mall")
#         self.textarea.insert(END,f"\n Bill Number : {self.bill_no.get()}")
#         self.textarea.insert(END,f"\n Customer Name : {self.c_name.get()}")
#         self.textarea.insert(END,f"\n Phone Number : {self.c_phone.get()}")
#         self.textarea.insert(END,f"\n Customer Email : {self.c_email.get()}")

#         self.textarea.insert(END,"\n ================================================" )
#         self.textarea.insert(END,f"\n Products\t\t\tQty\t\tPrice")
#         self.textarea.insert(END,"\n ================================================\n" )

#         self.l=[]
#     def AddItem(self):
#         Tax=5
#         self.n=self.prices.get()
#         self.m=self.qty.get()*self.n
#         self.l.append(self.m)
#         if self.product.get()=="":
#             messagebox.showerror("Error","Please Select the Product Name")
#         else:
#             self.subtot=sum(self.l)
#             self.taxx=(sum(self.l)*Tax)/100
#             self.totall=self.subtot+self.taxx
            
#             self.textarea.insert(END,f"\n {self.product.get()}\t\t\t{self.qty.get()}\t\t{self.m}")
#             self.sub_total.set(str("Rs.%.2f "%(self.subtot)))
#             self.tax_input.set(str("Rs.%.2f "%(self.taxx)))
#             self.total.set(str("Rs.%.2f "%(self.totall)))
    
#     def gen_bill(self):
#         if self.product.get()=="":
#             messagebox.showerror("Error","Please Add to Cart Product")
#         else:
#             text=self.textarea.get(10.0,(10.0+float(len(self.l))))
#             self.welcome()
#             self.textarea.insert(END,text)
#             self.textarea.insert(END,"\n ================================================" )
#             self.textarea.insert(END,f"\n Sub Amount:\t{self.sub_total.get()}")
#             self.textarea.insert(END,f"\n Tax Amount:\t{self.tax_input.get()}")
#             self.textarea.insert(END,f"\n Total Amount:\t{self.total.get()}")
#             self.textarea.insert(END,"\n ================================================" )

#     def save_bill(self):
#         op=messagebox.askyesno("Save Bill","Do You want Save this Bill")
#         if op>0:
#             self.bill_data=self.textarea.get(1.0,END)
#             f1=open('D:\\STOCK\\Capital_vercel1\\mksoftware\\bills/'+str(self.bill_no.get())+".txt",'w')
#             f1.write(self.bill_data)
#             op=messagebox.showinfo("Saved",f"Bill No : {self.bill_no.get()} saved successfully")
#             f1.close()

#     def iprint(self):
#         q=self.textarea.get(1.0,"end-1c")
#         filename=tempfile.mktemp('.txt')
#         open(filename,'w').write(q)
#         os.startfile(filename,"print")

#     def find_bill(self):
#         found="No"
#         for i in os.listdir("D:\\STOCK\\Capital_vercel1\\mksoftware\\bills/"):
#             if i.split('.')[0]==self.search_bill.get():
#                 f1=open(f"D:\\STOCK\\Capital_vercel1\\mksoftware\\bills/{i}",'r')
#                 self.textarea.delete(1.0,END)
#                 for d in f1:
#                     self.textarea.insert(END,d)
#                 f1.close()
#                 found="Yes"
#         if found=="No":
#             messagebox.showerror("Error","Invalid Bill No")

#     def clear(self):
#         self.textarea.delete(1.0,END)
#         self.c_name.set("")
#         self.c_phone.set("")
#         self.c_email.set("")
#         x=random.randint(1000,9999)
#         self.bill_no.set(str(x))
#         self.search_bill.set("")
#         self.product.set("")
#         self.prices.set(0)
#         self.qty.set(0)
#         self.l=[0]
#         self.total.set("")
#         self.sub_total.set("")
#         self.tax_input.set("")
#         self.welcome()

#     def Categories(self,event=""):        
#         if self.Combo_Category.get()=="Clothing":
#             self.ComboSubCategory.config(values=self.SubCatClothing)
#             self.ComboSubCategory.current(0)
#         if self.Combo_Category.get()=="LifeStyle":
#             self.ComboSubCategory.config(values=self.SubCatLifeSyyle)
#             self.ComboSubCategory.current(0)
#         if self.Combo_Category.get()=="Mobiles":
#             self.ComboSubCategory.config(values=self.SubCatMobile)
#             self.ComboSubCategory.current(0)

#     def Product_add(self,event=""):
#         if self.ComboSubCategory.get()=="Pant":
#             self.ComboProduct.config(values=self.pant)
#             self.ComboProduct.current(0)   
#         if self.ComboSubCategory.get()=="T-Shirt":
#             self.ComboProduct.config(values=self.t_shirt)
#             self.ComboProduct.current(0) 
#         if self.ComboSubCategory.get()=="Shirt":
#             self.ComboProduct.config(values=self.Shirt)
#             self.ComboProduct.current(0)  

#         #LifeStyle     
#         if self.ComboSubCategory.get()=="Bath Soap":
#             self.ComboProduct.config(values=self.Bath_soap)
#             self.ComboProduct.current(0) 
#         if self.ComboSubCategory.get()=="Face Cream":
#             self.ComboProduct.config(values=self.Face_cream)
#             self.ComboProduct.current(0)   
#         if self.ComboSubCategory.get()=="Hair Oil":
#             self.ComboProduct.config(values=self.hairoil)
#             self.ComboProduct.current(0)  

#         #Mobile
#         if self.ComboSubCategory.get()=="Iphone":
#             self.ComboProduct.config(values=self.Iphoe)
#             self.ComboProduct.current(0) 
#         if self.ComboSubCategory.get()=="Samsung":
#             self.ComboProduct.config(values=self.samsung)
#             self.ComboProduct.current(0)   
#         if self.ComboSubCategory.get()=="Xiome":
#             self.ComboProduct.config(values=self.xiome)
#             self.ComboProduct.current(0)      

#     def pricess(self,event=""):
#         #Pant
#         if self.ComboProduct.get()=="Levis":
#             self.ComboPrice.config(values=self.price_levis)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Mufti":
#             self.ComboPrice.config(values=self.price_mufti)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Spykar":
#             self.ComboPrice.config(values=self.price_spykar)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         #T-Shirt
#         if self.ComboProduct.get()=="Polo":
#             self.ComboPrice.config(values=self.price_polo)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Roadstar":
#             self.ComboPrice.config(values=self.price_roadstar)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Jack&Jones":
#             self.ComboPrice.config(values=self.price_JackJones)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         #Shirt
#         if self.ComboProduct.get()=="Peter England":
#             self.ComboPrice.config(values=self.price_PeterEngland)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Louis":
#             self.ComboPrice.config(values=self.price_Louis)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Park Acenue":
#             self.ComboPrice.config(values=self.price_Park)
#             self.ComboPrice.current(0)
#             self.qty.set(1)

#         #Bath Soap
#         if self.ComboProduct.get()=="Life Boy":
#             self.ComboPrice.config(values=self.price_lifeboy)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Lux":
#             self.ComboPrice.config(values=self.price_lux)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Santoor":
#             self.ComboPrice.config(values=self.price_santoor)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Pearl":
#             self.ComboPrice.config(values=self.price_pearl)
#             self.ComboPrice.current(0)
#             self.qty.set(1)

#         #Face Cream
#         if self.ComboProduct.get()=="Ponds":
#             self.ComboPrice.config(values=self.price_pond)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Borolin":
#             self.ComboPrice.config(values=self.price_borolin)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Herbel":
#             self.ComboPrice.config(values=self.price_herbel)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
            
#         #Hair Oil
#         if self.ComboProduct.get()=="Aavla":
#             self.ComboPrice.config(values=self.price_avala)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Coconut":
#             self.ComboPrice.config(values=self.price_coconut)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Sikakai":
#             self.ComboPrice.config(values=self.price_sikakai)
#             self.ComboPrice.current(0)
#             self.qty.set(1)

#         #Iphone
#         if self.ComboProduct.get()=="Iphone10":
#             self.ComboPrice.config(values=self.price_Iphone10)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Iphone11":
#             self.ComboPrice.config(values=self.price_Iphone11)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Iphone12":
#             self.ComboPrice.config(values=self.price_Iphone12)
#             self.ComboPrice.current(0)
#             self.qty.set(1)

#         #Samsung
#         if self.ComboProduct.get()=="SamsungA1":
#             self.ComboPrice.config(values=self.price_samsungA1)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="SamsungB12":
#             self.ComboPrice.config(values=self.price_samsungB12)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="SamsungC3":
#             self.ComboPrice.config(values=self.price_samsungC3)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
            
#         #Xiome
#         if self.ComboProduct.get()=="Xiome45":
#             self.ComboPrice.config(values=self.price_xiome45)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="Xiome90":
#             self.ComboPrice.config(values=self.price_xiome90)
#             self.ComboPrice.current(0)
#             self.qty.set(1)
#         if self.ComboProduct.get()=="XiomeNote":
#             self.ComboPrice.config(values=self.price_xiomeNote)
#             self.ComboPrice.current(0)
#             self.qty.set(1)

# if __name__== '__main__':
#     root=Tk()
#     obj=Bill_App(root)
#     root.mainloop()







# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.options.mode.chained_assignment = None

# con = urllib.parse.quote_plus(
#     'DRIVER={SQL Server Native Client 11.0};SERVER=MUKESH\SQLEXPRESS;DATABASE=BBCSORG;trusted_connection=yes')
# engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(con))

# sqlquery1 = ("select * from dbo.AgentMaster")
# ag_mas = pd.read_sql(sql=sqlquery1, con=engine)
# ag_mas = ag_mas[['AgCode', 'AgName']]

# sqlquery2 = ("select * from dbo.CompanyMaster")
# com_mas = pd.read_sql(sql=sqlquery2, con=engine)
# com_mas.rename({'CCode': 'Ccode'}, axis=1, inplace=True)
# com_mas = com_mas[['Ccode', 'BBCSShtName']]

# sqlquery3 = ("select * from dbo.GreyQualityNew")
# qlty_mas = pd.read_sql(sql=sqlquery3, con=engine)
# qlty_mas = qlty_mas[['QltyCode', 'QltyName', 'HSNCODE']]

# sqlquery4 = ("select * from dbo.SupplierMaster")
# sup_mas = pd.read_sql(sql=sqlquery4, con=engine)
# sup_mas = sup_mas[['SCode', 'SName', 'City', 'State', 'Mobile', 'GSTNONEW', 'Pincode']]

# sqlquery5 = ("select * from dbo.VoucherMaster")
# vou_mas = pd.read_sql(sql=sqlquery5, con=engine)
# vou_mas = vou_mas[vou_mas['VType1'] == 1]
# vou_mas.rename({'CCode': 'Ccode', 'VType2': 'InwChr'}, axis=1, inplace=True)
# vou_mas = vou_mas[['Ccode', 'InwChr', 'Module']]

# sqlquery6 = ("select * from dbo.InwardMaster")
# ind_mas = pd.read_sql(sql=sqlquery6, con=engine)
# # print(ind_mas.shape)

# merge = pd.merge(ind_mas, ag_mas, on=['AgCode'], how='left')
# merge = pd.merge(merge, com_mas, on=['Ccode'], how='left')
# merge = pd.merge(merge, qlty_mas, on=['QltyCode'], how='left')
# merge = pd.merge(merge, sup_mas, on=['SCode'], how='left')
# merge = pd.merge(merge, vou_mas, on=['Ccode', 'InwChr'], how='inner')
# # print(merge)
# merge = merge[
#     ['Ccode', 'InwChr', 'SCode', 'QltyCode', 'Fyear', 'BBCSShtName', 'Module', 'InwNo', 'InwDate', 'AgName', 'SName',
#      'FactCode', 'BillNo', 'QltyName', 'LrNo', 'Meter', 'GreyIssueMeter', 'RecvMtr', 'FoldMtr',
#      'ShortMtr', 'Unit', 'HSNCODE', 'BillRate', 'GrossAmt', 'NetAmt', 'BillAmount', 'PaidAmt',
#      'CGSTPER', 'CGSTAMT', 'SGSTPER', 'SGSTAMT', 'IGSTPER', 'IGSTAMT',
#      'OtherAdd', 'OtherDed', 'Packing', 'Freight', 'DisPer', 'DisAmt',
#      'TDSPer', 'TdsAmt2', 'TDSCode', 'Transport', 'Station',
#      'REVERCEPER', 'REVERCEAMT', 'IRNNO', 'ACKNO', 'ACKNODATE',
#      'City', 'State', 'Mobile', 'GSTNONEW', 'Pincode', 'Remark']]

# merge1 = copy(merge)
# merge1 = merge1[['Fyear', 'BBCSShtName', 'Module', 'InwNo', 'InwDate', 'SName', 'BillNo', 'GrossAmt', 'NetAmt']]
# year = [20212022, 20222023]
# merge1 = merge1[merge1.Fyear.isin(year)]
# col = ['GR', 'FP', 'ex', 'PP']
# merge2 = merge1[merge1.Module.isin(col)]
# run_tot = merge2.groupby(by=['BBCSShtName', 'SName']).sum()
# run_tot['result'] = np.where((run_tot['NetAmt'] > 5000000), True, False)
# merge3 = copy(merge2)
# merge3['InwMonth'] = np.where((merge3.InwDate.dt.strftime("%Y-%m") == '2021-04') |
#                               (merge3.InwDate.dt.strftime("%Y-%m") == '2021-05') |
#                               (merge3.InwDate.dt.strftime("%Y-%m") == '2021-06'),
#                               '2021-07', (merge3.InwDate.dt.strftime("%Y-%m")))
# merge3['Con'] = merge3['BBCSShtName'].astype(str) + '_' + merge3['SName']

# df = []

# for i in range(len(run_tot)):
#     if run_tot['result'].iloc[i]:
#         df.append(run_tot.iloc[i])
# df1 = pd.DataFrame(data=df)
# df1 = df1[['GrossAmt', 'NetAmt']]
# df1.reset_index(inplace=True)
# df1['Con'] = df1['level_0'].astype(str) + '_' + df1['level_1']

# df2 = copy(df1)
# df2 = pd.pivot_table(df2, 'NetAmt', index=['level_1'], columns=['level_0'], aggfunc=np.sum)

# df3 = df1['Con'].tolist()

# merge4 = merge3[merge3.Con.isin(df3)]

# merge5 = copy(merge4)
# merge5['SName1'] = merge5['SName'].str.replace(" ", "-")
# g = merge5.groupby(['BBCSShtName', 'SName1'])

# final = []
# for BBCSShtName, BBCSShtName_merge5 in g:
#     # print(BBCSShtName)
#     # print(BBCSShtName_merge5)
#     BBCSShtName_merge5["GrossSum"] = np.cumsum(BBCSShtName_merge5['GrossAmt'])
#     BBCSShtName_merge5["NetSum"] = np.cumsum(BBCSShtName_merge5['NetAmt'])
#     # mg = BBCSShtName_merge5.groupby(['BBCSShtName', 'SName'])[['GrossAmt', 'NetAmt']].cumsum()
#     # # merge5 = merge4.groupby(by=['BBCSShtName', 'SName', 'InwMonth']).sum()
#     BBCSShtName_merge5['Gross1'] = round((BBCSShtName_merge5['NetAmt'] / 105) * 100, 2)
#     BBCSShtName_merge5['Final'] = np.where((BBCSShtName_merge5['NetSum'] > 5000000),
#                                            round(BBCSShtName_merge5['Gross1'] * 0.001, 2), 0)

#     # print(BBCSShtName_merge5)
#     mg1 = BBCSShtName_merge5.groupby(by=['BBCSShtName', 'SName1', 'InwMonth']).sum()
#     mg1.reset_index(inplace=True)
#     #print(mg1)
#     final.append(mg1)
#     # # mg1 = mg.groupby(by=['BBCSShtName', 'SName1', 'InwMonth']).sum()
#     # # print(BBCSShtName_merge5)
#     #print(mg)
#     #print(mg1)

# string = ""
# for i in final:
#     string += str(i)



# print(string)

# # len = (len(final))
# # print(len)
# # f1 = pd.DataFrame(final)
# # print(f1[5])
# # print(final)
# # merge5.groupby(by=['BBCSShtName', 'SName1', 'InwMonth'])
# # print(merge5.head(50))
# # merge5["GrossSum"] = np.cumsum(merge5['GrossAmt'])
# # merge5["NetSum"] = np.cumsum(merge5['NetAmt'])
# # merge6 = merge5.groupby(by=['BBCSShtName', 'SName', 'InwMonth']).sum()
# # print(merge6.head(50))

# # merge5 = merge5[['Fyear', 'BBCSShtName', 'SName1', 'InwDate', 'InwMonth', 'GrossAmt', 'NetAmt']]
# # merge5 = pd.DataFrame(merge5)
# # merge5.sort_values(by=["BBCSShtName", "SName1"])
# # merge5['Con'] = merge5['BBCSShtName'] + '_' + merge5['SName1'] + '_' + merge5['InwDate'].astype(str)
# #
# # print(merge5.head(50))
# # merge5.set_index(merge5['Con'], inplace=True)
# # #merge5.sort_index('Con')
# # #merge6 = merge5.groupby('Con').cumsum()
# # merge6 = merge5.groupby(['BBCSShtName', 'SName1']).cumsum()
# # print(merge5.head(50))
# # print(merge5.shape)
# # print(merge6)
# if not os.path.exists("tds_sheet1.xlsx"):
#     try:
#         wb = xw.Book()
#         wb.sheets.add("total")
#         wb.sheets.add("tds1")
#         wb.sheets.add("tds2")
#         wb.sheets.add("tds3")
#         wb.sheets.add("tds4")
#         wb.save("tds_sheet1.xlsx")
#         wb.close()
#     except Exception as e:
#         print(f"Error Creating Excel File : {e}")

# wb = xw.Book("tds_sheet1.xlsx")
# tot = wb.sheets("total")
# tds1 = wb.sheets("tds1")
# tds2 = wb.sheets("tds2")
# tds3 = wb.sheets("tds3")
# tds4 = wb.sheets("tds4")

# tot.range("a:cc").value = None
# tot.range("a1").value = pd.DataFrame(merge3)
# tds1.range("a:cc").value = None
# tds1.range("a1").value = pd.DataFrame(run_tot)
# tds2.range("a:cc").value = None
# tds2.range("a1").value = pd.DataFrame(df2)
# tds3.range("a:cc").value = None
# tds3.range("a1").value = merge5
# tds4.range("a:cc").value = None
# tds4.range("a1").value = merge
# # tds3.range("a1").value = final
# # tds3.range("A1").options(pd.DataFrame).value = final
# # tds3.range("a1").value = final

