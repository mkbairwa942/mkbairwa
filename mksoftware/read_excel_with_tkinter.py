from tkinter import *
import tkinter as tk
import pandas as pd
from tkinter import ttk,filedialog
from sqlalchemy import create_engine
import urllib

con = urllib.parse.quote_plus(
    'DRIVER={SQL Server Native Client 11.0};SERVER=MUKESH\SQLEXPRESS;DATABASE=BBCSORG;trusted_connection=yes')
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(con))

sqlquery1 = ("select * from dbo.AgentMaster")
ag_ma = pd.read_sql(sql=sqlquery1, con=engine)
df1 = ag_ma[['AgCode', 'AgName','City','Mobile','PanNo']]

root =Tk()
root.title("Excel")
root.geometry("700x700")

my_frame = Frame(root)
my_frame.pack(pady=20)

my_tree = ttk.Treeview(my_frame)
def file_open():
    filename=filedialog.askopenfilename(initialdir="D:/STOCK",
                                        title="Open A File",
                                        filetypes=(("xlsx files","*.xlsx"),("All Files","*.*"),("Csv Files",".csv")))
    if filename:
        try:
            filename = r"{}".format(filename)
            df = pd.read_excel(filename)
        except ValueError:
            my_label.config(text="File Could Not be Open")
        except FileNotFoundError:
            my_label.config(text="File Could Not be found")
    clear_tree()

    my_tree["column"] = list(df1.columns)
    my_tree["show"] = "headings"
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(",",font=('Helvetica',11))
    s.configure("Treeview.Heading",foreground='red',font=('Helvetica',11,"bold"))
    for column in my_tree["column"]:
        my_tree.heading(column,text=column,anchor=tk.CENTER)
        my_tree.column(column,width=200,minwidth=50,anchor=tk.CENTER)

    df_rows = df1.to_numpy().tolist()
    for row in df_rows:
        my_tree.insert("","end",values=row)

    hsb =ttk.Scrollbar(my_frame,orient="horizontal")
    hsb.configure(command=my_tree.xview)
    my_tree.configure(xscrollcommand=hsb.set)
    hsb.pack(fill="x",side="bottom")

    vsb =ttk.Scrollbar(my_frame,orient="vertical")
    vsb.configure(command=my_tree.yview)
    my_tree.configure(yscrollcommand=vsb.set)
    vsb.pack(fill="y",side="right")
    my_tree.pack()



def clear_tree():
    my_tree.delete(*my_tree.get_children())

my_menu = Menu(root)
root.config(menu=my_menu)
file_menu=Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Spreadsheets",menu=file_menu)
file_menu.add_command(label="Open",command=file_open)


my_label = Label(root,text='')
my_label.pack(pady=20)

root.mainloop()
