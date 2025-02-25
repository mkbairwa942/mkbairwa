from tkinter import *
from tkinter import ttk

# import tkinter as tk
# from tkinter import ttk,filedialog
# import ttkbootstrap as ttk
# from ttkbootstrap.tableview import Tableview
# from ttkbootstrap.constants import *
from sqlalchemy import create_engine
import urllib
import random,os
from tkinter import messagebox
import tempfile
import pandas as pd
from time import strftime

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

con = urllib.parse.quote_plus(
    'DRIVER={SQL Server Native Client 11.0};SERVER=MUKESH\SQLEXPRESS;DATABASE=BBCSORG;trusted_connection=yes')
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(con))

sup_mas_query = ("select * from dbo.SupplierMaster")
sup_mas = pd.read_sql(sql=sup_mas_query, con=engine)

sub_group_query = ("select * from dbo.SubGroupMaster")
sub_group = pd.read_sql(sql=sub_group_query, con=engine)
sub_group.rename({'SGCODE': 'SgCode'}, axis=1, inplace=True)


agent_query = ("select * from dbo.AgentMaster")
agent = pd.read_sql(sql=agent_query, con=engine)
agent = agent[['AgCode','AgName', 'Mobile']]
agent.rename({'AgCode': 'AGCode'}, axis=1, inplace=True)

sup_masss = sup_mas[['SCode','SName']]
sup_masss.rename({'SCode': 'PGCode'}, axis=1, inplace=True)

sup_mas1 = pd.merge(sup_mas, sub_group, on=['SgCode'], how='left')
sup_mas2 = pd.merge(sup_mas1, agent, on=['AGCode'], how='left')
sup_mas_new = pd.merge(sup_mas2, sup_masss, on=['PGCode'], how='left')

#sup_mas_new = sup_mas
class Account_App:
    def __init__(self,root):
        self.root=root
        self.root.geometry("900x650+240+30")
        self.root.title("Account Master")
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        fieldbackground="D3D3D3")
        style.map("Treeview",
                  background=[("selected","#347083")])
        
        #Variables
        self.party_code=StringVar()
        self.sub_group_code=StringVar()
        self.agent_code=StringVar()
        self.party_group_code=StringVar()
        self.serachh_name=StringVar()

        self.party_name=StringVar()
        self.sub_group=StringVar()
        self.agent_name=StringVar()
        self.party_group=StringVar()

        self.address1=StringVar()
        self.address2=StringVar()
        self.address3=StringVar()
        self.city=StringVar()
        self.state=StringVar()
        self.transport=StringVar()
        self.ac_lock=StringVar()
        self.payment_terms=StringVar()
        self.phone_1=StringVar()
        self.Mobile_1=StringVar()
        self.Mobile_2=StringVar()
        self.email=StringVar()
        self.pincode=IntVar()
        self.credit_days=IntVar()
        self.interest_rate=IntVar()
        self.discount=IntVar()
        self.belong_to=StringVar()
        self.radio_button = StringVar()

        self.pan_no=StringVar()
        self.limit_amount=IntVar()
        self.GSTIN=StringVar()
 

        self.Main_Frame=Frame(self.root,relief=GROOVE)
        self.Main_Frame.place(x=0,y=5,width=900,height=600)

        self.Time_label = ttk.Label(self.Main_Frame, font=('digital-7', 25), background='black', foreground='magenta')
        self.Time_label.place(x=790,y=5,width=100,height=40)
        self.time()

        self.lbl_name=Label(self.Main_Frame,text="Party Name")
        self.lbl_name.grid(row=0,column=0,sticky=W,padx=5)
        self.entry_code=Entry(self.Main_Frame,textvariable=self.party_code,font=("arial",9,"bold"),width=12)
        self.entry_code.grid(row=0,column=1,sticky=W,padx=3,pady=1)
        self.entry_name=Entry(self.Main_Frame,textvariable=self.party_name,font=("arial",9,"bold"),width=60)
        self.entry_name.grid(row=0,column=1,sticky=W,padx=95,pady=1)

        self.lbl_sub_group=Label(self.Main_Frame,text="Sub Group")
        self.lbl_sub_group.grid(row=1,column=0,sticky=W,padx=3)
        self.entry_sub_gcode=Entry(self.Main_Frame,textvariable=self.sub_group_code,font=("arial",9,"bold"),width=12)
        self.entry_sub_gcode.grid(row=1,column=1,sticky=W,padx=3,pady=1)
        self.entry_sub_group=Entry(self.Main_Frame,textvariable=self.sub_group,font=("arial",9,"bold"),width=60)
        self.entry_sub_group.grid(row=1,column=1,sticky=W,padx=95,pady=1)

        self.lbl_agent=Label(self.Main_Frame,text="Agent Name")
        self.lbl_agent.grid(row=2,column=0,sticky=W,padx=3)
        self.entry_acode=Entry(self.Main_Frame,textvariable=self.agent_code,font=("arial",9,"bold"),width=12)
        self.entry_acode.grid(row=2,column=1,sticky=W,padx=3,pady=1)
        self.entry_agent=Entry(self.Main_Frame,textvariable=self.agent_name,font=("arial",9,"bold"),width=60)
        self.entry_agent.grid(row=2,column=1,sticky=W,padx=95,pady=1)

        self.lbl_party_group=Label(self.Main_Frame,text="Party Group")
        self.lbl_party_group.grid(row=3,column=0,sticky=W,padx=3)
        self.entry_party_gcode=Entry(self.Main_Frame,textvariable=self.party_group_code,font=("arial",9,"bold"),width=12)
        self.entry_party_gcode.grid(row=3,column=1,sticky=W,padx=3,pady=1)
        self.entry_party_group=Entry(self.Main_Frame,textvariable=self.party_group,font=("arial",9,"bold"),width=60)
        self.entry_party_group.grid(row=3,column=1,sticky=W,padx=95,pady=1)

        self.lbl_address=Label(self.Main_Frame,text="Address")
        self.lbl_address.grid(row=4,column=0,sticky=W,padx=3,pady=(15,1))
        self.entry_address=ttk.Entry(self.Main_Frame,textvariable=self.address1,font=("arial",9,"bold"),width=62)
        self.entry_address.grid(row=4,column=1,columnspan=3,sticky=W,padx=3,pady=(15,1))
        self.entry_address2=Entry(self.Main_Frame,textvariable=self.address2,font=("arial",9,"bold"),width=62)
        self.entry_address2.grid(row=5,column=1,columnspan=3,sticky=W,padx=3,pady=1)
        self.entry_address3=Entry(self.Main_Frame,textvariable=self.address3,font=("arial",9,"bold"),width=62)
        self.entry_address3.grid(row=6,column=1,columnspan=3,sticky=W,padx=3,pady=1)

        self.lbl_city=Label(self.Main_Frame,text="City")
        self.lbl_city.grid(row=7,column=0,sticky=W,padx=1,pady=(15,2))
        self.entry_city=Entry(self.Main_Frame,textvariable=self.city,font=("arial",9,"bold"),width=30)
        self.entry_city.grid(row=7,column=1,sticky=W,padx=1,pady=(15,2))

        self.lbl_pincode=Label(self.Main_Frame,text="Pincode")
        self.lbl_pincode.grid(row=7,column=1,sticky=W,padx=220,pady=(15,2))
        self.entry_pincode=Entry(self.Main_Frame,textvariable=self.pincode,font=("arial",9,"bold"),width=15)
        self.entry_pincode.grid(row=7,column=1,sticky=W,padx=330,pady=(15,2))

        self.lbl_state=Label(self.Main_Frame,text="State")
        self.lbl_state.grid(row=8,column=0,sticky=W,padx=1)
        self.entry_state=Entry(self.Main_Frame,textvariable=self.state,font=("arial",9,"bold"),width=30)
        self.entry_state.grid(row=8,column=1,sticky=W,padx=1)

        self.lbl_C_days=Label(self.Main_Frame,text="Credit Days")
        self.lbl_C_days.grid(row=8,column=1,sticky=W,padx=220)
        self.entry_C_days=Entry(self.Main_Frame,textvariable=self.credit_days,font=("arial",9,"bold"),width=15)
        self.entry_C_days.grid(row=8,column=1,sticky=W,padx=330)

        self.lbl_transport=Label(self.Main_Frame,text="Transport")
        self.lbl_transport.grid(row=9,column=0,sticky=W,padx=1)
        self.entry_transport=Entry(self.Main_Frame,textvariable=self.transport,font=("arial",9,"bold"),width=30)
        self.entry_transport.grid(row=9,column=1,sticky=W,padx=1)

        self.lbl_Int_rate=Label(self.Main_Frame,text="Int. Rate (%)")
        self.lbl_Int_rate.grid(row=9,column=1,sticky=W,padx=220)
        self.entry_Int_rate=Entry(self.Main_Frame,textvariable=self.interest_rate,font=("arial",9,"bold"),width=15)
        self.entry_Int_rate.grid(row=9,column=1,sticky=W,padx=330)

        self.lbl_ac_lock=Label(self.Main_Frame,text="Ac Lock")
        self.lbl_ac_lock.grid(row=10,column=0,sticky=W,padx=1)
        self.entry_ac_lock=Entry(self.Main_Frame,textvariable=self.ac_lock,font=("arial",9,"bold"),width=30)
        self.entry_ac_lock.grid(row=10,column=1,sticky=W,padx=1)

        self.lbl_discount=Label(self.Main_Frame,text="Discount (%)")
        self.lbl_discount.grid(row=10,column=1,sticky=W,padx=220)
        self.entry_discount=Entry(self.Main_Frame,textvariable=self.discount,font=("arial",9,"bold"),width=15)
        self.entry_discount.grid(row=10,column=1,sticky=W,padx=330)

        self.lbl_remarks=Label(self.Main_Frame,text="Remarks")
        self.lbl_remarks.grid(row=11,column=0,sticky=W,padx=1)
        self.entry_remarks=Entry(self.Main_Frame,textvariable=self.payment_terms,font=("arial",9,"bold"),width=109)
        self.entry_remarks.grid(row=11,column=1,sticky=W,padx=1,pady=(10,2))

        
        self.belong_to_frame=LabelFrame(self.Main_Frame,text="Belongs To",border=2)
        self.belong_to_frame.place(x=570,y=5,width=180,height=80)

        # self.belong = ['General','Purchase','Sales']

        # for bel in self.belong:
        self.radio_general=ttk.Radiobutton(self.belong_to_frame,command=self.radio_button_get, text="General",variable=self.radio_button,value="GEN").pack(anchor=W,padx=5)
        self.radio_pur=ttk.Radiobutton(self.belong_to_frame,command=self.radio_button_get, text="Purchase",variable=self.radio_button,value="PUR").pack(anchor=W,padx=5)
        self.radio_sale=ttk.Radiobutton(self.belong_to_frame,command=self.radio_button_get, text="Sales",variable=self.radio_button,value="SAL").pack(anchor=W,padx=5)
        
        self.lbl_limita_amt=Label(self.Main_Frame,text="Limit Amt")
        self.lbl_limita_amt.grid(row=4,column=1,sticky=W,padx=465,pady=(15,1))
        self.entry_limita_amt=Entry(self.Main_Frame,textvariable=self.limit_amount,font=("arial",9,"bold"),width=30)
        self.entry_limita_amt.grid(row=4,column=1,sticky=W,padx=555,pady=(15,1))
        
        
        self.lbl_pan_no=Label(self.Main_Frame,text="Pan No.")
        self.lbl_pan_no.grid(row=5,column=1,sticky=W,padx=465)
        self.entry_pan_no=Entry(self.Main_Frame,textvariable=self.pan_no,font=("arial",9,"bold"),width=30)
        self.entry_pan_no.grid(row=5,column=1,sticky=W,padx=555)

        self.lbl_GSTIN=Label(self.Main_Frame,text="GSTIN NO")
        self.lbl_GSTIN.grid(row=6,column=1,sticky=W,padx=465)
        self.entry_GSTIN=Entry(self.Main_Frame,textvariable=self.GSTIN,font=("arial",9,"bold"),width=30)
        self.entry_GSTIN.grid(row=6,column=1,sticky=W,padx=555)        

        self.lbl_phone_1=Label(self.Main_Frame,text="Phone No")
        self.lbl_phone_1.grid(row=7,column=1,sticky=W,padx=465,pady=(15,2))
        self.entry_phone_1=Entry(self.Main_Frame,textvariable=self.phone_1,font=("arial",9,"bold"),width=30)
        self.entry_phone_1.grid(row=7,column=1,sticky=W,padx=555,pady=(15,2))

        self.lbl_Mobile_1=Label(self.Main_Frame,text="Mobile_1")
        self.lbl_Mobile_1.grid(row=8,column=1,sticky=W,padx=465)
        self.entry_Mobile_1=Entry(self.Main_Frame,textvariable=self.Mobile_1,font=("arial",9,"bold"),width=30)
        self.entry_Mobile_1.grid(row=8,column=1,sticky=W,padx=555)

        self.lbl_Mobile_2=Label(self.Main_Frame,text="Mobile_2")
        self.lbl_Mobile_2.grid(row=9,column=1,sticky=W,padx=465)
        self.entry_Mobile_2=Entry(self.Main_Frame,textvariable=self.Mobile_2,font=("arial",9,"bold"),width=30)
        self.entry_Mobile_2.grid(row=9,column=1,sticky=W,padx=555)

        self.lbl_email_id=Label(self.Main_Frame,text="Email Id")
        self.lbl_email_id.grid(row=10,column=1,sticky=W,padx=465)
        self.entry_email_id=Entry(self.Main_Frame,textvariable=self.email,font=("arial",9,"bold"),width=30)
        self.entry_email_id.grid(row=10,column=1,sticky=W,padx=555)      
      
        self.my_table_frame=ttk.LabelFrame(self.root,text="Table Area",border=2)
        self.my_table_frame.place(x=5,y=390,width=890,height=250)

        tree_scrolly = Scrollbar(self.my_table_frame,orient="vertical")
        tree_scrolly.pack(side="right",fill="y")
        
        tree_scrollx = Scrollbar(self.my_table_frame,orient="horizontal")
        tree_scrollx.pack(side="bottom",fill="x")

        self.my_tree = ttk.Treeview(self.my_table_frame,yscrollcommand=tree_scrolly.set,xscrollcommand=tree_scrollx.set,selectmode="extended")
        self.my_tree.pack()
        tree_scrolly.config(command=self.my_tree.yview)
        tree_scrollx.config(command=self.my_tree.xview)

        self.my_tree["column"] = list(sup_mas_new.columns)
        self.my_tree["show"] = "headings"
        # s = ttk.Style(root)
        # s.theme_use("clam")
        # s.configure(",",font=('Helvetica',11))
        # s.configure("Treeview.Heading",foreground='red',font=('Helvetica',11,"bold"))
        for column in self.my_tree["column"]:
            self.my_tree.heading(column,text=column,anchor=CENTER)
            if column == "SName":
                self.my_tree.column(column,width=180,minwidth=50,stretch=NO,anchor=W)
            else:
                self.my_tree.column(column,width=180,minwidth=50,stretch=NO,anchor=CENTER)

        self.my_tree.tag_configure("oddrow",background="white")
        self.my_tree.tag_configure("evenrow",background="lightblue")

        global count
        count = 0

        df_rows = sup_mas_new.to_numpy().tolist()
        for row in df_rows:
            if count % 2 ==0:
                self.my_tree.insert(parent="",index="end",iid=count,text="",values=row,tags=('evenrow',))
            else:
                self.my_tree.insert(parent="",index="end",iid=count,text="",values=row,tags=('oddrow',))
            count +=1

        Btn_Frame=ttk.LabelFrame(root,text="Button", )
        Btn_Frame.place(x=100,y=320,width=710,height=60)

        self.entry_Search=ttk.Entry(Btn_Frame,textvariable=self.serachh_name,font=("arial",10,"bold"),width=24)
        self.entry_Search.grid(row=0,column=1,sticky=W,padx=2)
        
        self.BtnSearch=ttk.Button(Btn_Frame,command=self.find_bill,width=15,text="Search",cursor="hand2")
        self.BtnSearch.grid(row=0,column=2,sticky=W,padx=7)

        self.BtnAddToCart=ttk.Button(Btn_Frame,command=self.Save,width=8,text="Save",cursor="hand2")
        self.BtnAddToCart.grid(row=0,column=3)

        self.BtnGenBill=ttk.Button(Btn_Frame,command=self.New,width=8,text="New",cursor="hand2")
        self.BtnGenBill.grid(row=0,column=4)

        self.BtnSaveBill=ttk.Button(Btn_Frame,command=self.Delete,width=8,text="Delete",cursor="hand2")
        self.BtnSaveBill.grid(row=0,column=5)

        self.BtnPrint=ttk.Button(Btn_Frame,command=self.Print,width=8,text="Print",cursor="hand2")
        self.BtnPrint.grid(row=0,column=6)

        self.BtnExit=ttk.Button(Btn_Frame,command=self.root.destroy,width=8,text="Exit",cursor="hand2")
        self.BtnExit.grid(row=0,column=7)

        self.my_tree.bind("<ButtonRelease-1>",self.select_record)

    def radio_button_get(self):
        selection = "You selected the option " +self.radio_button.get()
        print(selection)

    def clear_records(self):
        self.entry_code.delete(0,END)
        self.entry_name.delete(0,END)
        self.entry_sub_gcode.delete(0,END)
        self.entry_sub_group.delete(0,END)
        self.entry_acode.delete(0,END)
        self.entry_agent.delete(0,END)
        self.entry_party_gcode.delete(0,END)
        self.entry_party_group.delete(0,END)
        self.entry_address.delete(0,END)
        self.entry_address2.delete(0,END)
        self.entry_address3.delete(0,END)
        self.entry_city.delete(0,END)
        self.entry_pincode.delete(0,END)
        self.entry_state.delete(0,END)
        self.entry_C_days.delete(0,END)
        self.entry_transport.delete(0,END)
        self.entry_Int_rate.delete(0,END)
        self.entry_ac_lock.delete(0,END)
        self.entry_discount.delete(0,END)
        self.entry_remarks.delete(0,END)
        self.entry_limita_amt.delete(0,END)
        self.entry_pan_no.delete(0,END)
        self.entry_GSTIN.delete(0,END)
        self.entry_phone_1.delete(0,END)
        self.entry_Mobile_1.delete(0,END)
        self.entry_Mobile_2.delete(0,END)
        self.entry_email_id.delete(0,END)
        self.entry_Search.delete(0,END)

    def select_record(self,e):
        
        self.clear_records()
        selected = self.my_tree.focus()
        values = self.my_tree.item(selected,'values')

        self.entry_code.insert(0,values[0])
        self.entry_name.insert(0,values[1])
        self.entry_sub_gcode.insert(0,values[2])
        self.entry_sub_group.insert(0,values[39])
        self.entry_acode.insert(0,values[4])
        self.entry_agent.insert(0,values[41])
        self.entry_party_gcode.insert(0,values[6])
        self.entry_party_group.insert(0,values[43])
        self.entry_address.insert(0,values[7])
        self.entry_address2.insert(0,values[8])
        self.entry_address3.insert(0,values[9])
        self.entry_city.insert(0,values[10])
        self.entry_pincode.insert(0,values[11])
        self.entry_state.insert(0,values[12])
        self.entry_C_days.insert(0,values[3])
        self.entry_transport.insert(0,values[20])
        self.entry_Int_rate.insert(0,values[22])
        self.entry_ac_lock.insert(0,values[34])
        self.entry_discount.insert(0,values[36])
        self.entry_remarks.insert(0,values[32])
        self.entry_limita_amt.insert(0,values[29])
        self.entry_pan_no.insert(0,values[13])
        self.entry_GSTIN.insert(0,values[35])
        self.entry_phone_1.insert(0,values[16])
        self.entry_Mobile_1.insert(0,values[17])
        self.entry_Mobile_2.insert(0,values[18])
        self.entry_email_id.insert(0,values[19])
        

    # def Save(self):
    #     self.clear_records()

    def New(self):
        self.clear_records()

    def Save(self):
        selected = self.my_tree.focus()
        #self.my_tree.item(selected,text="",values=(self.entry_email_id.get(),self.entry_Mobile_2.get(),))

        sup_mas_query = ("select * from dbo.SupplierMaster")
        sup_mas = pd.read_sql(sql=sup_mas_query, con=engine)

        sub_group_query = ("select * from dbo.SubGroupMaster")
        sub_group = pd.read_sql(sql=sub_group_query, con=engine)
        sub_group.rename({'SGCODE': 'SgCode'}, axis=1, inplace=True)


        agent_query = ("select * from dbo.AgentMaster")
        agent = pd.read_sql(sql=agent_query, con=engine)
        agent = agent[['AgCode','AgName', 'Mobile']]
        agent.rename({'AgCode': 'AGCode'}, axis=1, inplace=True)

        sup_masss = sup_mas[['SCode','SName']]
        sup_masss.rename({'SCode': 'PGCode'}, axis=1, inplace=True)

        sup_mas1 = pd.merge(sup_mas, sub_group, on=['SgCode'], how='left')
        sup_mas2 = pd.merge(sup_mas1, agent, on=['AGCode'], how='left')
        sup_mas_new = pd.merge(sup_mas2, sup_masss, on=['PGCode'], how='left')

        updateee = ("update dbo.SupplierMaster set Pincode  = 382447 where SCode = 9717")

        update_database = ("""
                           update dbo.SupplierMaster set
                            SName = self.entry_name.get(),
                            SgCode = self.entry_sub_gcode,
                            CreditDays = self.entry_C_days,
                            AGCode = self.entry_acode,
                            PGCode = self.entry_party_gcode,
                            Add1 = self.entry_address,
                            Add2 = self.entry_address2,
                            Add3 = self.entry_address3,
                            City = self.entry_city,
                            Pincode = self.entry_pincode,
                            State = self.entry_state,
                            PanNo = self.entry_pan_no,
                            OPhone = self.entry_phone_1,
                            RPhone = self.entry_Mobile_1,
                            Mobile = self.entry_Mobile_2,
                            Email = self.entry_email_id,
                            Transport = self.entry_transport,
                            IntRate = self.entry_Int_rate,
                            LimitAmount = self.entry_limita_amt,
                            PaymentWeek =self.entry_remarks,
                            AccountCheck = self.entry_ac_lock,
                            GSTNONEW =self.entry_GSTIN,,
                            DiscountPer = self.entry_discount
                            where SCode = self.entry_code.get()
                           """)

        self.clear_records()

    def Delete(self):
        x = self.my_tree.selection()[0]
        self.my_tree.delete(x)
        self.clear_records()

    def Delete_one(self):
        x = self.my_tree.selection()
        for record in x:
            self.my_tree.delete(record)
            self.clear_records()

    def Delete_all(self):
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
            self.clear_records()

    def Print(self):
        q=self.party_nam_query1.get(1.0,"end-1c")
        filename=tempfile.mktemp('.csv')
        open(filename,'w').write(q)
        os.startfile(filename,"print")

    def find_bill(self):
        party_nam = self.serachh_name.get()
        self.party_nam_query = ("select * from dbo.SupplierMaster WHERE SName LIKE '%"+party_nam+"%'")
        self.party_nam = pd.read_sql(sql=self.party_nam_query, con=engine)

        sub_group_query = ("select * from dbo.SubGroupMaster")
        sub_group = pd.read_sql(sql=sub_group_query, con=engine)
        sub_group.rename({'SGCODE': 'SgCode'}, axis=1, inplace=True)


        agent_query = ("select * from dbo.AgentMaster")
        agent = pd.read_sql(sql=agent_query, con=engine)
        agent = agent[['AgCode','AgName', 'Mobile']]
        agent.rename({'AgCode': 'AGCode'}, axis=1, inplace=True)

        sup_masss = sup_mas[['SCode','SName']]
        sup_masss.rename({'SCode': 'PGCode'}, axis=1, inplace=True)

        sup_mas1 = pd.merge(self.party_nam, sub_group, on=['SgCode'], how='left')
        sup_mas2 = pd.merge(sup_mas1, agent, on=['AGCode'], how='left')
        self.party_nam_new = pd.merge(sup_mas2, sup_masss, on=['PGCode'], how='left')

        self.update_tree(self.party_nam_new)
   

    def update_tree(self,party_nam_new):
        self.my_tree.delete(*self.my_tree.get_children())     
        self.my_tree["column"] = list(self.party_nam_new.columns)
        self.my_tree["show"] = "headings"
        # s = ttk.Style(root)
        # s.theme_use("clam")
        # s.configure(",",font=('Helvetica',11))
        # s.configure("Treeview.Heading",foreground='red',font=('Helvetica',11,"bold"))
        for column in self.my_tree["column"]:
            self.my_tree.heading(column,text=column,anchor=CENTER)
            if column == "SName":
                self.my_tree.column(column,width=180,minwidth=50,stretch=NO,anchor=W)
            else:
                self.my_tree.column(column,width=180,minwidth=50,stretch=NO,anchor=CENTER)
        
        self.my_tree.tag_configure("oddrow",background="white")
        self.my_tree.tag_configure("evenrow",background="lightblue")

        global count1
        count1 = 0

        df_rows1 = party_nam_new.to_numpy().tolist()
        for rows in df_rows1:
            self.my_tree.insert("","end",values=rows)

        # hsb =ttk.Scrollbar(self.my_table_frame,orient="horizontal")
        # hsb.configure(command=self.my_tree.xview)
        # self.my_tree.configure(xscrollcommand=hsb.set)
        # hsb.pack(fill="x",side="bottom")
        # vsb =ttk.Scrollbar(self.my_table_frame,orient="vertical")
        # vsb.configure(command=self.my_tree.yview)
        # self.my_tree.configure(yscrollcommand=vsb.set)
        # vsb.pack(fill="y",side="right")
        # self.my_tree.pack()

    def time(self):
        #string = strftime('%H:%M:%S %p')
        string = strftime('%H:%M:%S')
        self.Time_label.config(text=string)
        self.Time_label.after(50, self.time)

light_theme = ["cosmo","flatly","journal","litera","lumen","minty","pulse","sandstone","united","yeti","morph","simplex","cerculean"]
dark_theme = ["solar","superhero","darkly","cyborg","vapor",""]

if __name__== '__main__':
    root=Tk()
    obj=Account_App(root)
    # root = ttk.Window(themename="flatly")
    root.mainloop()

        # #Product Categories
        # self.Category=["Select Option","Clothing","LifeStyle","Mobiles"]
        # self.SubCatClothing=["Pant","T-Shirt","Shirt"]
        # self.pant=["Levis","Mufti","Spykar"]
        # self.price_levis=5000
        # self.price_mufti=700
        # self.price_spykar=8000

        # self.t_shirt=["Polo","Roadstar","Jack&Jones"]
        # self.price_polo=1500
        # self.price_roadstar=1800
        # self.price_JackJones=1700

        # self.Shirt=["Peter England","Louis","Park Acenue"]
        # self.price_PeterEngland=2100
        # self.price_Louis=2700
        # self.price_Park=1740

        # self.SubCatLifeSyyle=["Bath Soap","Face Cream","Hair Oil"]
        # self.Bath_soap=["Life Boy","Lux","Santoor","Pearl"]
        # self.price_lifeboy=20
        # self.price_lux=25
        # self.price_santoor=30
        # self.price_pearl=50

        # self.Face_cream=["Ponds","Borolin","Herbel"]
        # self.price_pond=50
        # self.price_borolin=30
        # self.price_herbel=90     

        # self.hairoil=["Aavla","Coconut","Sikakai"]
        # self.price_avala=50
        # self.price_coconut=60
        # self.price_sikakai=70

        # self.SubCatMobile=["Iphone","Samsung","Xiome"]
        # self.Iphoe=["Iphone10","Iphone11","Iphone12"]
        # self.price_Iphone10=50000
        # self.price_Iphone11=60000
        # self.price_Iphone12=70000

        # self.samsung=["SamsungA1","SamsungB12","SamsungC3"]
        # self.price_samsungA1=40000
        # self.price_samsungB12=16000
        # self.price_samsungC3=26000

        # self.xiome=["Xiome45","Xiome90","XiomeNote"]
        # self.price_xiome45= 27000
        # self.price_xiome90=35000
        # self.price_xiomeNote=60000

    #     # Image1
    #     img1=Image.open("D:\STOCK\Capital_vercel1\mksoftware\image/image1.jpg")
    #     img1=img1.resize((850,130),Image.Resampling.HAMMING)
    #     self.photoimg1=ImageTk.PhotoImage(img1)

    #     lbl_img1=Label(self.root,image=self.photoimg1)
    #     lbl_img1.place(x=0,y=0,width=850,height=130)

    #     # Image3
    #     img2=Image.open("D:\STOCK\Capital_vercel1\mksoftware\image/image5.jpg")
    #     img2=img2.resize((850,130),Image.Resampling.HAMMING)
    #     self.photoimg2=ImageTk.PhotoImage(img2)

    #     # Heading
    #     lbl_img2=Label(self.root,image=self.photoimg2)
    #     lbl_img2.place(x=500,y=0,width=850,height=130)

    #     lbl_title=Label(self.root,text="BILLING SOFTWARE USING PYTHON",font=("times new roman",35,"bold"),bg="white",fg="red")
    #     lbl_title.place(x=0,y=130,width=1360,height=45)

    #             #time
    #     def time():
    #         string=strftime('%H:%M:%S %p')
    #         lbl.config(text=string)
    #         lbl.after(1000,time)

    #     lbl=Label(lbl_title,font=("arial",15,"bold"),fg="blue",bg="white")
    #     lbl.place(x=5,y=0,width=120,height=50)
    #     time()

    #     # self.Main_Frame
    #     self.Main_Frame=Frame(self.root,bd=5,relief=GROOVE,bg="white")
    #     self.Main_Frame.place(x=0,y=175,width=1360,height=520)
        
    #     # Customer_Frame
    #     Cust_Frame=LabelFrame(self.Main_Frame,text="Customer",font=("times new roman",12,"bold"),bg="white",fg="red")
    #     Cust_Frame.place(x=10,y=5,width=300,height=140)

    #     # Custome_frame_Deatils
    #     self.lbl_mob=Label(Cust_Frame,font=("arial",11,"bold"),bg="white",text="Mobile No",bd=4)
    #     self.lbl_mob.grid(row=0,column=0,sticky=W,padx=8,pady=5)

    #     self.entry_mob=ttk.Entry(Cust_Frame,textvariable=self.c_phone,font=("arial",10,"bold"),width=18)
    #     self.entry_mob.grid(row=0,column=1,sticky=W,padx=8,pady=5)

    #     self.lbl_name=Label(Cust_Frame,font=("arial",11,"bold"),bg="white",text="Customer Name",bd=4)
    #     self.lbl_name.grid(row=1,column=0,sticky=W,padx=8,pady=5)

    #     self.entry_name=ttk.Entry(Cust_Frame,textvariable=self.c_name,font=("arial",10,"bold"),width=18)
    #     self.entry_name.grid(row=1,column=1,sticky=W,padx=8,pady=5)

    #     self.lbl_email=Label(Cust_Frame,font=("arial",11,"bold"),bg="white",text="Customer Email",bd=4)
    #     self.lbl_email.grid(row=2,column=0,sticky=W,padx=8,pady=5)

    #     self.entry_email=ttk.Entry(Cust_Frame,textvariable=self.c_email,font=("arial",10,"bold"),width=18)
    #     self.entry_email.grid(row=2,column=1,sticky=W,padx=8,pady=5)

    #     # Product Label_Frame
    #     Prod_Frame=LabelFrame(self.Main_Frame,text="Product",font=("times new roman",12,"bold"),bg="white",fg="red")
    #     Prod_Frame.place(x=320,y=5,width=540,height=140)

    #     # Category
    #     self.lblCategory=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Select Categories",bd=4)
    #     self.lblCategory.grid(row=0,column=0,sticky=W,padx=8,pady=5)

    #     self.Combo_Category=ttk.Combobox(Prod_Frame,values=self.Category,font=("arial",10,"bold"),width=18,state="readonly")
    #     self.Combo_Category.current(0)
    #     self.Combo_Category.grid(row=0,column=1,sticky=W,padx=8,pady=5,)
    #     self.Combo_Category.bind("<<ComboboxSelected>>",self.Categories)

    #     # SubCategory
    #     self.lblSubCategory=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Subcategory",bd=4)
    #     self.lblSubCategory.grid(row=1,column=0,sticky=W,padx=8,pady=5)

    #     self.ComboSubCategory=ttk.Combobox(Prod_Frame,values=[""],font=("arial",10,"bold"),width=18,state="readonly")
    #     self.ComboSubCategory.grid(row=1,column=1,sticky=W,padx=8,pady=5)
    #     self.ComboSubCategory.bind("<<ComboboxSelected>>",self.Product_add)

    #     # Product Name
    #     self.lblproduct=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Product Name",bd=4)
    #     self.lblproduct.grid(row=2,column=0,sticky=W,padx=8,pady=5)

    #     self.ComboProduct=ttk.Combobox(Prod_Frame,textvariable=self.product,font=("arial",10,"bold"),width=18,state="readonly")
    #     self.ComboProduct.grid(row=2,column=1,sticky=W,padx=8,pady=5)
    #     self.ComboProduct.bind("<<ComboboxSelected>>",self.pricess)

    #     # Price
    #     self.lblPrice=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Price",bd=4)
    #     self.lblPrice.grid(row=0,column=2,sticky=W,padx=8,pady=5)

    #     self.ComboPrice=ttk.Combobox(Prod_Frame,textvariable=self.prices,font=("arial",10,"bold"),width=18,state="readonly")
    #     self.ComboPrice.grid(row=0,column=3,sticky=W,padx=8,pady=5)

    #     # Quantity
    #     self.lblQty=Label(Prod_Frame,font=("arial",10,"bold"),bg="white",text="Qty",bd=4)
    #     self.lblQty.grid(row=1,column=2,sticky=W,padx=8,pady=5)

    #     self.ComboQty=ttk.Entry(Prod_Frame,textvariable=self.qty,font=("arial",10,"bold"),width=20)
    #     self.ComboQty.grid(row=1,column=3,sticky=W,padx=8,pady=5)

    #     #Middle Frame
    #     Middle_Frame=Frame(self.Main_Frame,bd=10,bg="white")
    #     Middle_Frame.place(x=10,y=150,width=848,height=240)

    #     imgMiddle1=Image.open("D:\STOCK\Capital_vercel1\mksoftware\image/image1.jpg")
    #     imgMiddle1=imgMiddle1.resize((426,250),Image.Resampling.HAMMING)
    #     self.photoimg3=ImageTk.PhotoImage(imgMiddle1)

    #     lbl_img1=Label(Middle_Frame,image=self.photoimg3)
    #     lbl_img1.place(x=0,y=0,width=426,height=250)

    #     imgMiddle2=Image.open("D:\STOCK\Capital_vercel1\mksoftware\image/image5.jpg")
    #     imgMiddle2=imgMiddle2.resize((426,250),Image.Resampling.HAMMING)
    #     self.photoimg4=ImageTk.PhotoImage(imgMiddle2)

    #     lbl_img2=Label(Middle_Frame,image=self.photoimg4)
    #     lbl_img2.place(x=400,y=0,width=426,height=250)

    #     # Search Area
    #     Search_Frame=Frame(self.Main_Frame,bd=2,bg="white")
    #     Search_Frame.place(x=870,y=10,width=500,height=35)

    #     self.lblBill=Label(Search_Frame,font=("arial",10,"bold"),fg="white",bg="red",text="Bill Number")
    #     self.lblBill.grid(row=0,column=0,sticky=W,padx=4,pady=4)
        
    #     self.entry_Search=ttk.Entry(Search_Frame,textvariable=self.search_bill,font=("arial",10,"bold"),width=24)
    #     self.entry_Search.grid(row=0,column=1,sticky=W,padx=2)
        
    #     self.BtnSearch=Button(Search_Frame,command=self.find_bill,width=15,text="Search",font=('arial',10,'bold'),bg="orangered",fg="white",cursor="hand2")
    #     self.BtnSearch.grid(row=0,column=2,sticky=W,padx=7)

    #     # Right frame Bill Area
    #     RightLabelFrame=LabelFrame(self.Main_Frame,text="Bill Area",font=("times new roman",12,"bold"),bg="white",fg="red")
    #     RightLabelFrame.place(x=870,y=45,width=470,height=350)

    #     scroll_y=Scrollbar(RightLabelFrame,orient=VERTICAL)
    #     self.textarea=Text(RightLabelFrame,yscrollcommand=scroll_y.set,bg="white",fg="blue",font=("times new roman",12,"bold"))
    #     scroll_y.pack(side=RIGHT,fill=Y)
    #     scroll_y.config(command=self.textarea.yview)
    #     self.textarea.pack(fill=BOTH,expand=1)

    #     # Bill Counter Label_Frame
    #     Bottom_Frame=LabelFrame(self.Main_Frame,text="Bill Counter",font=("times new roman",12,"bold"),bg="white",fg="red")
    #     Bottom_Frame.place(x=0,y=395,width=1345,height=115)

        
    #     # Sub Total
    #     self.lblSubTotal=Label(Bottom_Frame,font=("arial",10,"bold"),bg="white",text="Sub Total",bd=4)
    #     self.lblSubTotal.grid(row=0,column=0,sticky=W,padx=5,pady=2)

    #     self.EntrySubTotal=ttk.Entry(Bottom_Frame,textvariable=self.sub_total,font=("arial",10,"bold"),width=20)
    #     self.EntrySubTotal.grid(row=0,column=1,sticky=W,padx=5,pady=2)

    #     # Taxes
    #     self.lblTax=Label(Bottom_Frame,font=("arial",10,"bold"),bg="white",text="GST",bd=4)
    #     self.lblTax.grid(row=1,column=0,sticky=W,padx=5,pady=2)

    #     self.EntryTax=ttk.Entry(Bottom_Frame,textvariable=self.tax_input,font=("arial",10,"bold"),width=20)
    #     self.EntryTax.grid(row=1,column=1,sticky=W,padx=5,pady=2)

    #     # Amount
    #     self.lblAmount=Label(Bottom_Frame,font=("arial",10,"bold"),bg="white",text="Net Amount",bd=4)
    #     self.lblAmount.grid(row=2,column=0,sticky=W,padx=5,pady=2)

    #     self.EntryAmount=ttk.Entry(Bottom_Frame,textvariable=self.total,font=("arial",10,"bold"),width=20)
    #     self.EntryAmount.grid(row=2,column=1,sticky=W,padx=5,pady=2)

    #     # Button Frame
    #     Btn_Frame=Frame(Bottom_Frame,bd=2,bg="white")
    #     Btn_Frame.place(x=260,y=0)

    #     self.BtnAddToCart=Button(Btn_Frame,command=self.AddItem,height=2,width=14,text="Add to Cart",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
    #     self.BtnAddToCart.grid(row=0,column=0)

    #     self.BtnGenBill=Button(Btn_Frame,command=self.gen_bill,height=2,width=14,text="Generate Bill",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
    #     self.BtnGenBill.grid(row=0,column=1)

    #     self.BtnSaveBill=Button(Btn_Frame,command=self.save_bill,height=2,width=14,text="Save Bill",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
    #     self.BtnSaveBill.grid(row=0,column=2)

    #     self.BtnPrint=Button(Btn_Frame,height=2,command=self.iprint,width=14,text="Print",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
    #     self.BtnPrint.grid(row=0,column=3)

    #     self.BtnClear=Button(Btn_Frame,command=self.clear,height=2,width=14,text="Clear",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
    #     self.BtnClear.grid(row=0,column=4)

    #     self.BtnExit=Button(Btn_Frame,command=self.root.destroy,height=2,width=14,text="Exit",font=('arial',15,'bold'),bg="orangered",fg="white",cursor="hand2")
    #     self.BtnExit.grid(row=0,column=5)
    #     self.welcome()
    # # ===function Declaration====

    # def welcome(self):
    #     self.textarea.delete(1.0,END)
    #     self.textarea.insert(END,"\t Welcome Codewith Mukesh Mini Mall")
    #     self.textarea.insert(END,f"\n Bill Number : {self.bill_no.get()}")
    #     self.textarea.insert(END,f"\n Customer Name : {self.c_name.get()}")
    #     self.textarea.insert(END,f"\n Phone Number : {self.c_phone.get()}")
    #     self.textarea.insert(END,f"\n Customer Email : {self.c_email.get()}")

    #     self.textarea.insert(END,"\n ================================================" )
    #     self.textarea.insert(END,f"\n Products\t\t\tQty\t\tPrice")
    #     self.textarea.insert(END,"\n ================================================\n" )

    #     self.l=[]
    # def AddItem(self):
    #     Tax=5
    #     self.n=self.prices.get()
    #     self.m=self.qty.get()*self.n
    #     self.l.append(self.m)
    #     if self.product.get()=="":
    #         messagebox.showerror("Error","Please Select the Product Name")
    #     else:
    #         self.subtot=sum(self.l)
    #         self.taxx=(sum(self.l)*Tax)/100
    #         self.totall=self.subtot+self.taxx
            
    #         self.textarea.insert(END,f"\n {self.product.get()}\t\t\t{self.qty.get()}\t\t{self.m}")
    #         self.sub_total.set(str("Rs.%.2f "%(self.subtot)))
    #         self.tax_input.set(str("Rs.%.2f "%(self.taxx)))
    #         self.total.set(str("Rs.%.2f "%(self.totall)))
    
    # def gen_bill(self):
    #     if self.product.get()=="":
    #         messagebox.showerror("Error","Please Add to Cart Product")
    #     else:
    #         text=self.textarea.get(10.0,(10.0+float(len(self.l))))
    #         self.welcome()
    #         self.textarea.insert(END,text)
    #         self.textarea.insert(END,"\n ================================================" )
    #         self.textarea.insert(END,f"\n Sub Amount:\t{self.sub_total.get()}")
    #         self.textarea.insert(END,f"\n Tax Amount:\t{self.tax_input.get()}")
    #         self.textarea.insert(END,f"\n Total Amount:\t{self.total.get()}")
    #         self.textarea.insert(END,"\n ================================================" )

    # def save_bill(self):
    #     op=messagebox.askyesno("Save Bill","Do You want Save this Bill")
    #     if op>0:
    #         self.bill_data=self.textarea.get(1.0,END)
    #         f1=open('D:\\STOCK\\Capital_vercel1\\mksoftware\\bills/'+str(self.bill_no.get())+".txt",'w')
    #         f1.write(self.bill_data)
    #         op=messagebox.showinfo("Saved",f"Bill No : {self.bill_no.get()} saved successfully")
    #         f1.close()

    # def iprint(self):
    #     q=self.textarea.get(1.0,"end-1c")
    #     filename=tempfile.mktemp('.txt')
    #     open(filename,'w').write(q)
    #     os.startfile(filename,"print")

    # def find_bill(self):
    #     found="No"
    #     for i in os.listdir("D:\\STOCK\\Capital_vercel1\\mksoftware\\bills/"):
    #         if i.split('.')[0]==self.search_bill.get():
    #             f1=open(f"D:\\STOCK\\Capital_vercel1\\mksoftware\\bills/{i}",'r')
    #             self.textarea.delete(1.0,END)
    #             for d in f1:
    #                 self.textarea.insert(END,d)
    #             f1.close()
    #             found="Yes"
    #     if found=="No":
    #         messagebox.showerror("Error","Invalid Bill No")

    # def clear(self):
    #     self.textarea.delete(1.0,END)
    #     self.c_name.set("")
    #     self.c_phone.set("")
    #     self.c_email.set("")
    #     x=random.randint(1000,9999)
    #     self.bill_no.set(str(x))
    #     self.search_bill.set("")
    #     self.product.set("")
    #     self.prices.set(0)
    #     self.qty.set(0)
    #     self.l=[0]
    #     self.total.set("")
    #     self.sub_total.set("")
    #     self.tax_input.set("")
    #     self.welcome()

    # def Categories(self,event=""):        
    #     if self.Combo_Category.get()=="Clothing":
    #         self.ComboSubCategory.config(values=self.SubCatClothing)
    #         self.ComboSubCategory.current(0)
    #     if self.Combo_Category.get()=="LifeStyle":
    #         self.ComboSubCategory.config(values=self.SubCatLifeSyyle)
    #         self.ComboSubCategory.current(0)
    #     if self.Combo_Category.get()=="Mobiles":
    #         self.ComboSubCategory.config(values=self.SubCatMobile)
    #         self.ComboSubCategory.current(0)

    # def Product_add(self,event=""):
    #     if self.ComboSubCategory.get()=="Pant":
    #         self.ComboProduct.config(values=self.pant)
    #         self.ComboProduct.current(0)   
    #     if self.ComboSubCategory.get()=="T-Shirt":
    #         self.ComboProduct.config(values=self.t_shirt)
    #         self.ComboProduct.current(0) 
    #     if self.ComboSubCategory.get()=="Shirt":
    #         self.ComboProduct.config(values=self.Shirt)
    #         self.ComboProduct.current(0)  

    #     #LifeStyle     
    #     if self.ComboSubCategory.get()=="Bath Soap":
    #         self.ComboProduct.config(values=self.Bath_soap)
    #         self.ComboProduct.current(0) 
    #     if self.ComboSubCategory.get()=="Face Cream":
    #         self.ComboProduct.config(values=self.Face_cream)
    #         self.ComboProduct.current(0)   
    #     if self.ComboSubCategory.get()=="Hair Oil":
    #         self.ComboProduct.config(values=self.hairoil)
    #         self.ComboProduct.current(0)  

    #     #Mobile
    #     if self.ComboSubCategory.get()=="Iphone":
    #         self.ComboProduct.config(values=self.Iphoe)
    #         self.ComboProduct.current(0) 
    #     if self.ComboSubCategory.get()=="Samsung":
    #         self.ComboProduct.config(values=self.samsung)
    #         self.ComboProduct.current(0)   
    #     if self.ComboSubCategory.get()=="Xiome":
    #         self.ComboProduct.config(values=self.xiome)
    #         self.ComboProduct.current(0)      

    # def pricess(self,event=""):
    #     #Pant
    #     if self.ComboProduct.get()=="Levis":
    #         self.ComboPrice.config(values=self.price_levis)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Mufti":
    #         self.ComboPrice.config(values=self.price_mufti)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Spykar":
    #         self.ComboPrice.config(values=self.price_spykar)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     #T-Shirt
    #     if self.ComboProduct.get()=="Polo":
    #         self.ComboPrice.config(values=self.price_polo)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Roadstar":
    #         self.ComboPrice.config(values=self.price_roadstar)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Jack&Jones":
    #         self.ComboPrice.config(values=self.price_JackJones)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     #Shirt
    #     if self.ComboProduct.get()=="Peter England":
    #         self.ComboPrice.config(values=self.price_PeterEngland)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Louis":
    #         self.ComboPrice.config(values=self.price_Louis)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Park Acenue":
    #         self.ComboPrice.config(values=self.price_Park)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)

    #     #Bath Soap
    #     if self.ComboProduct.get()=="Life Boy":
    #         self.ComboPrice.config(values=self.price_lifeboy)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Lux":
    #         self.ComboPrice.config(values=self.price_lux)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Santoor":
    #         self.ComboPrice.config(values=self.price_santoor)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Pearl":
    #         self.ComboPrice.config(values=self.price_pearl)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)

    #     #Face Cream
    #     if self.ComboProduct.get()=="Ponds":
    #         self.ComboPrice.config(values=self.price_pond)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Borolin":
    #         self.ComboPrice.config(values=self.price_borolin)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Herbel":
    #         self.ComboPrice.config(values=self.price_herbel)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
            
    #     #Hair Oil
    #     if self.ComboProduct.get()=="Aavla":
    #         self.ComboPrice.config(values=self.price_avala)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Coconut":
    #         self.ComboPrice.config(values=self.price_coconut)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Sikakai":
    #         self.ComboPrice.config(values=self.price_sikakai)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)

    #     #Iphone
    #     if self.ComboProduct.get()=="Iphone10":
    #         self.ComboPrice.config(values=self.price_Iphone10)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Iphone11":
    #         self.ComboPrice.config(values=self.price_Iphone11)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Iphone12":
    #         self.ComboPrice.config(values=self.price_Iphone12)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)

    #     #Samsung
    #     if self.ComboProduct.get()=="SamsungA1":
    #         self.ComboPrice.config(values=self.price_samsungA1)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="SamsungB12":
    #         self.ComboPrice.config(values=self.price_samsungB12)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="SamsungC3":
    #         self.ComboPrice.config(values=self.price_samsungC3)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
            
    #     #Xiome
    #     if self.ComboProduct.get()=="Xiome45":
    #         self.ComboPrice.config(values=self.price_xiome45)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="Xiome90":
    #         self.ComboPrice.config(values=self.price_xiome90)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)
    #     if self.ComboProduct.get()=="XiomeNote":
    #         self.ComboPrice.config(values=self.price_xiomeNote)
    #         self.ComboPrice.current(0)
    #         self.qty.set(1)








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

