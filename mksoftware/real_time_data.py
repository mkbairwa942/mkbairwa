import tkinter as tk
from tkinter import ttk
import sqlite3
from sqlalchemy import create_engine
import urllib
import pandas as pd
from datetime import date
import xlwings as xw
import os
import numpy as np

root = tk.Tk()
root.geometry("600x350")

con = urllib.parse.quote_plus(
    'DRIVER={SQL Server Native Client 11.0};SERVER=MUKESH\SQLEXPRESS;DATABASE=BBCSORG;trusted_connection=yes')
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(con))

sqlquery1 = ("select * from dbo.AgentMaster")
ag_ma = pd.read_sql(sql=sqlquery1, con=engine)
ag_ma = ag_ma[['AgCode', 'AgName','City','Mobile','PanNo']]

print(ag_ma.tail(3))
#ag_mas = pd.DataFrame(data=ag_ma)
stk_list = np.unique(ag_ma['AgCode'])

eq_data_pd = pd.DataFrame()
for i in stk_list:
    eq_data1 = ag_ma[ag_ma['AgCode'] == i]
    # print(eq_data1)
    eq_data_pd = pd.concat([eq_data1, eq_data_pd])

tree = ttk.Treeview(root)
tree['show']='headings'
s = ttk.Style(root)
s.theme_use("clam")
s.configure(",",font=('Helvetica',11))
s.configure("Treeview.Heading",foreground='red',font=('Helvetica',11,"bold"))
tree["columns"] = ("AgCode","AgName","City","Mobile","PanNo")

tree.column("AgCode",width=50,minwidth=50,anchor=tk.CENTER)
tree.column("AgName",width=50,minwidth=50,anchor=tk.CENTER)
tree.column("City",width=50,minwidth=50,anchor=tk.CENTER)
tree.column("Mobile",width=50,minwidth=50,anchor=tk.CENTER)
tree.column("PanNo",width=50,minwidth=50,anchor=tk.CENTER)

tree.heading("AgCode",text="AgCode",anchor=tk.CENTER)
tree.heading("AgName",text="AgName",anchor=tk.CENTER)
tree.heading("City",text="City",anchor=tk.CENTER)
tree.heading("Mobile",text="Mobile",anchor=tk.CENTER)
tree.heading("PanNo",text="PanNo",anchor=tk.CENTER)

i=0
for ro in eq_data_pd:
    print(ro)
    tree.insert('','end',text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4]))
    i=i+1

hsb =ttk.Scrollbar(root,orient="horizontal")
hsb.configure(command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(fill="x",side="bottom")
tree.pack()

root.mainloop()

# def addDb():
#     conn=sqlite3.connect("stockmarket.db")
#     stockList=stockName.get().split(",")
#     for name in stockList:
#         conn.execute("insert into stocks(name,indices) values('"+name+"','"+indices.get()+"')")
#     conn.commit()
#     conn.close()
#     print("DB UPDATED")

# def refreshTable(event):
#     i=0
#     conn=sqlite3.connect("stockmarket.db")
#     cursor=conn.execute("select * from stocks where indices='"+indices.get()+"'")
#     for row in cursor:
#         ttk.Label(scrollableFrame,text=row[0],width=15,font=("Time New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=0)
#         ttk.Label(scrollableFrame,text="",width=15,font=("Time New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=1)
#         ttk.Label(scrollableFrame,text="",width=15,font=("Time New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=2)
#         ttk.Label(scrollableFrame,text="",width=15,font=("Time New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=3)
#         ttk.Label(scrollableFrame,text="",width=15,font=("Time New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=4)
#         ttk.Label(scrollableFrame,text="",width=15,font=("Time New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=5)
#         i+=1

# def clearWidgets():
#     widgets=scrollableFrame.winfo_children()
#     i=0
#     while(i<len(widgets)):
#         widgets[i].destroy()
#         i+=1


# topFrame  = Frame(root)
# Button(topFrame,text="CONTACT").grid(row=0,column=0)
# Label(topFrame,text='INDEX').grid(row=0,column=1)
# indices=ttk.Combobox(topFrame,values=["NIFTY 50","NIFTY BANK","NIFTY IT","NIFTY ENERGY"],width=15,font=("Arial Bold",10))
# indices.bind("<<ComboboxSelected>>",refreshTable)
# indices.grid(row=0,column=2)
# Label(topFrame,text="NAME").grid(row=0,column=3)
# stockName=Entry(topFrame)
# stockName.grid(row=0,column=4)
# Button(topFrame,text="ADD TO DB").grid(row=0,column=5)
# Button(topFrame,text="START").grid(row=0,column=6)
# Button(topFrame,text="STOP").grid(row=0,column=7)
# topFrame.pack()

# titleFrame=Frame(root)
# Label(titleFrame,text="NAME",width=13,font=("Times New Roman bold",10)).grid(row=0,column=0)
# Label(titleFrame,text="HIGH",width=13,font=("Times New Roman bold",10)).grid(row=0,column=1)
# Label(titleFrame,text="LOW",width=13,font=("Times New Roman bold",10)).grid(row=0,column=2)
# Label(titleFrame,text="LTP",width=13,font=("Times New Roman bold",10)).grid(row=0,column=3)
# Label(titleFrame,text="VOLUME",width=13,font=("Times New Roman bold",10)).grid(row=0,column=4)
# Label(titleFrame,text="CHANGE",width=13,font=("Times New Roman bold",10)).grid(row=0,column=5)
# titleFrame.pack()

# botFrame=Frame()
# canvas=Canvas(botFrame)
# scrollbar=ttk.Scrollbar(botFrame,orient="vertical",command=canvas.yview)
# scrollableFrame=ttk.Frame(canvas)
# scrollableFrame.bind("<<configure>>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
# canvas.create_window((0,0),window=scrollableFrame,anchor="nw")
# canvas.configure(width=580,yscrollcommand=scrollbar.set)
# botFrame.pack()
# canvas.pack(side="left",fill="both",expand=True)
# scrollbar.pack(side="right",fill="y")

# root.mainloop()