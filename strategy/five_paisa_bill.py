import pandas as pd
import copy
import numpy as np
import xlwings as xw
from time import sleep
from datetime import date, datetime, timedelta
from dateutil.utils import today
import PyPDF2
from PyPDF2 import PdfFileMerger,PdfReader
#import pdfplumber
#from dateparser.search import search_dates
from os import listdir
from os.path import isfile, join
from pathlib import Path
#import pikepdf
import os
import tabula
import time,json,datetime,sys

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

#path = "E:/STOCK/five_paisa_bill/Document.pdf"
path = "E:/STOCK/five_paisa_bill1/2023-05-22.pdf"

def fetch_all_pdf_files(parent_folder: str):
    target_files = []
    for path, subdirs, files in os.walk(parent_folder):
        for name in files:
            if name.endswith(".pdf"):
                target_files.append(os.path.join(path,name))
    return target_files

# def merge_pdf(list_of_pdfs,output_filename="final_merged_file.pdf"):
#     merger = PyPDF2.PdfMerger()
#     with open(output_filename,"wb") as f:
#         for file in list_of_pdfs:
#             merger.append(file)
#         merger.write(f)
# pdf_list = fetch_all_pdf_files("E:/STOCK/five_paisa_bill")
# output_file = merge_pdf(pdf_list)
# print(output_file)

# filee = PyPDF2.PdfReader(path,password="CIWPB5219G")
# totalpages = int(len(filee.pages))
# print(totalpages)


def extract_text(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path,password="CIWPB5219G")
    result = []
    for i in range(0,len(reader.pages)):
        selected_page = reader.pages[i]
        text = selected_page.extract_text()
        result.append(text)
    return " ".join(result)

text = extract_text(path)
datee = (text[(text.find("Date:"))+5:(text.find("Date:"))+16])
date_time_obj = datetime.datetime.strptime(datee, '%b %d %Y')
# print(date_time_obj)

# with pdfplumber.open(path,password="CIWPB5219G") as f:
#     for i in f.pages:
#         fp = (i.extract_text())



# files_dir = fetch_all_pdf_files("E:/STOCK/five_paisa_bill1")
# print(files_dir)

summaryy = pd.DataFrame()
ledger = pd.DataFrame()

# for file in files_dir:
#     print(file)
    
summary = pd.DataFrame()
text1 = extract_text(path)
# print(text1)
dateey = (text1[(text1.find("Date:"))+5:(text1.find("Date:"))+16])
date_time_obj1 = datetime.datetime.strptime(dateey, '%b %d %Y')

dff = tabula.io.read_pdf(path,pages="all",password="CIWPB5219G")
tot_df = len(dff)
print(tot_df)
print(date_time_obj1)

if tot_df <= 2:
    print("No. 1")
    print(str(tot_df)+" Pages")
    df = dff[1]
    rslt = df[df["Trade"] != "Time"]
    rslt_df = rslt[rslt["Trade"].notnull()]
    #rslt_df = (df[df[df.columns[3]].notnull() ])[(df[df[df.columns[3]].notnull() ])[(df[df[df.columns[3]].notnull() ]).columns[6]].notnull() ]
    rslt_df['Date'] = date_time_obj1
    rslt_df = rslt_df[['Date', 'Trade','Security / Contract', 'Buy(B)/', 'Quantity',
                    'Gross Rate/.1','Brokerage','Net Rate','Closing Rate Per','STT','Net Total']]
    summary = pd.concat([rslt_df, summary])

if tot_df > 2 and tot_df <= 3:
    print("No. 2")
    print(str(tot_df)+" Pages")
    df = pd.concat([dff[1], dff[2]], ignore_index=True)
    #df5 = df[df["Trade"].notnull()]
    rslt = df[df["Trade"] != "Time"]
    rslt_df = rslt[rslt["Trade"].notnull()]
    #rslt_df = (df[df[df.columns[3]].notnull() ])[(df[df[df.columns[3]].notnull() ])[(df[df[df.columns[3]].notnull() ]).columns[6]].notnull() ]
    rslt_df['Date'] = date_time_obj1
    rslt_df = rslt_df[['Date', 'Trade','Security / Contract', 'Buy(B)/', 'Quantity',
                    'Gross Rate/.1','Brokerage','Net Rate','Closing Rate Per','STT','Net Total']]
    summary = pd.concat([rslt_df, summary])

if tot_df > 3:
    print("No. 3")
    print(str(tot_df)+" Pages")
    df = pd.concat([dff[1], dff[2], dff[3]], ignore_index=True)
    #df5 = df[df["Trade"].notnull()]
    rslt = df[df["Trade"] != "Time"]
    rslt_df = rslt[rslt["Trade"].notnull()]
    #rslt_df = (df[df[df.columns[3]].notnull() ])[(df[df[df.columns[3]].notnull() ])[(df[df[df.columns[3]].notnull() ]).columns[6]].notnull() ]
    rslt_df['Date'] = date_time_obj1
    rslt_df = rslt_df[['Date', 'Trade','Security / Contract', 'Buy(B)/', 'Quantity',
                    'Gross Rate/.1','Brokerage','Net Rate','Closing Rate Per','STT','Net Total']]
    summary = pd.concat([rslt_df, summary])

for col in  summary.columns[5:]:
    summary[col] = pd.to_numeric(summary[col], errors='coerce')

STT_val = 0.0152
Ex_Tr_Ch = 0.00061
SEBI_Turn = 0.01
IGST = 0.18
Stamp_Du = 0.01


Datee = pd.to_datetime(summary['Date'].iloc[-1]).date()
STT = summary[summary["Buy(B)/"] == "SELL"]
STT_Total = np.round(((STT["STT"]).sum()),1)
Brok = summary[summary["Brokerage"] != 0]
Brok_Total = np.round(abs(Brok["Net Total"].sum()),2)
Exch_Trans_Chg = summary[summary["Buy(B)/"] == "SELL"]
Exch_Trans_Chg_Total = np.round((((Exch_Trans_Chg["Net Total"])*Ex_Tr_Ch).sum()),2).item()
SEBI_Turn_chg = summary[summary["Buy(B)/"] == "SELL"]
SEBI_Turn_Total = np.round(((SEBI_Turn_chg["Net Rate"].count())*SEBI_Turn),2)
Taxable_value = np.round((Brok_Total+Exch_Trans_Chg_Total+SEBI_Turn_Total),2)
IGST_Total = np.round((Taxable_value*IGST),2)
Stamp_Dut = summary[summary["Buy(B)/"] == "SELL"]
Stamp_Dut1 = np.round(((Stamp_Dut["Net Total"]).sum()),1)
Net_Total = (summary["Net Total"]).sum()


if Stamp_Dut1 >= 10000:
    Stamp_Duty = 1
else:
    Stamp_Duty = 0

if Net_Total > 0:
    Net_Amount = np.round((Net_Total-(STT_Total+Exch_Trans_Chg_Total+IGST_Total+SEBI_Turn_Total+Stamp_Duty)),2)
else:
    Net_Amount = np.round((Net_Total-(STT_Total+Exch_Trans_Chg_Total+IGST_Total+SEBI_Turn_Total+Stamp_Duty)),2)

dataa = [[Datee,STT_Total,Brok_Total,Exch_Trans_Chg_Total,SEBI_Turn_Total,Taxable_value,IGST_Total,Stamp_Duty,Net_Total,Net_Amount]]
Lederr = pd.DataFrame(dataa, columns=['Datee','STT_Total','Brok_Total','Exch_Trans_Chg_Total','SEBI_Turn_Total','Taxable_value','IGST_Total','Stamp_Duty','Net_Total','Net_Amount'])
print(Lederr)
summaryy = pd.concat([summary, summaryy])
ledger = pd.concat([Lederr, ledger])

# print(Datee)
# print(STT_Total)
# print(Brok_Total)
# print(Exch_Trans_Chg_Total)
# print(SEBI_Turn_Total)
# print(Taxable_value) 
# print(IGST_Total)
# print(Stamp_Duty)
# print(Net_Total)
# print(Net_Amount)

print("Excel Starting....")
if not os.path.exists("five_paisa_bill.xlsx"):
    try:
        wb = xw.Book()
        wb.save("five_paisa_bill.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('five_paisa_bill.xlsx')
for i in ["Data","Summary","Ledger","Extra"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
sum = wb.sheets("Summary")
ldg = wb.sheets("Ledger")
ext = wb.sheets("Extra")
dt.range("a:z").value = None
sum.range("a:r").value = None
ldg.range("a:z").value = None
ext.range("a:z").value = None

try:
    time.sleep(0.5)
    dt.range("a1").value = df
    sum.range("a1").value = summaryy
    ldg.range("a1").value = ledger
    ext.range("a1").value = rslt


except Exception as e:
    print(e)



# filename = open("E:/STOCK/five_paisa_bill/Document.pdf","rb")
# reader = PyPDF2.PdfReader(filename)
# if reader.is_encrypted:
#     reader.decrypt('CIWPB5219G')
#     page1 = reader.pages[0]
#     print(len(reader.pages))
#     pdfdata=page1.extract_text()
#     print(pdfdata)

#     info = reader.metadata
#     print(info)

# df = read_pdf("E:/STOCK/five_paisa_bill/Document.pdf")
# print(df)












# # Make a list of absolute path's to all of the PDF files in the target folder
# files = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and join(path, f).endswith('.pdf')]

# Iterate through the list of PDF files using the PDF's aboslute path

# for f in files:
#     with open(f, 'rb') as file_handle:
#         # Set strict=False to allow PDF files that don't comply to the PDF spec: https://www.pdfa.org/resource/pdf-specification-index/
#         pdf_reader = PyPDF2.PdfFileReader(file_handle, strict=False)
#         page_text = ''
#         # Iterate through each page in the PDF document to extract the text and add to plain-text string
#         for page_num in range(0, pdf_reader.getNumPages()):
#             page = pdf_reader.getPage(page_num)
#             page_text += page.extract_text()
#     # Write the plain text string to a file with the same name
#     with open(f.replace('.pdf', '.txt'), 'a+') as text_file_handle:
#         text_file_handle.writelines(page_text)


# ENCRYPTED_FILE_PATH = 'E:/STOCK/five_paisa_bill/Document.pdf'

# with open(ENCRYPTED_FILE_PATH, mode='rb') as f:        
#     reader = PyPDF2.PdfReader(f)
#     if reader.is_encrypted:
#         reader.decrypt('CIWPB5219G')
#         print(f"Number of page: {reader.getNumPages()}")



# reader = PyPDF2.PdfReader(filename)
# page1 = reader.pages[0]
# print(len(reader.pages))
# pdfdata=page1.extract_text()
# print(pdfdata)

# pdf = pikepdf.open('E:/STOCK/five_paisa_bill/Document.pdf',password="CIWPB5219G")
# pdf.save('extractable.pdf')


       








