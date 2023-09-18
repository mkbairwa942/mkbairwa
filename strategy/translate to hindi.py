from englisttohindi.englisttohindi import EngtoHindi
from googletrans import Translator
# from pushbullet import PushBullet
import pywhatkit as pwk
import pyautogui as gui
import time
import emoji

# == Read PDF == 


# message = "Yes, I am geeks" 
# res = EngtoHindi(message)
# print(res.convert)

# == Read PDF and convert to hindi ==

# from PyPDF2 import PdfReader
# #file=open("E:\STOCK\THE MAN WHO SOLVE THE MARKET.pdf",'rb')
# file=open("E:\STOCK\Ahmedabad_LL_Swati___Gunjan_Jain_V2 (1).pdf",'rb')
# reader=PdfReader(file)
# num_pages=len(reader.pages)

# for p in range(num_pages):
#     page=reader.pages[p]
#     text=page.extract_text()
#     #print(text)
#     from googletrans import Translator
#     #translator=Translator()
#     translator = Translator(service_urls=['translate.googleapis.com'])
#     translate_text=translator.translate(text,dest='hi')
    #print(translate_text)
    # res = EngtoHindi(text)
    # print(res.convert)

# == Send notification to phone using push bullet == 

# API_KEY = "o.fvzu6cfmMRHxfy2HWmfrjd5gUezubnxP"
# file = 'E:/STOCK/Capital_vercel1/strategy/text_file.txt'
# with open(file,mode='r') as f:
#     text1 = f.read()

# pb = PushBullet(API_KEY)
# #push = pb.push_note("Please Remember","will you remember me")
# push = pb.push_note("Please Remember",text1)

# Send message using whats app ==

#pwk.sendwhatmsg("+919610033622","HI I Am Mukesh How are you 1",10,True,10)
pwk.sendwhatmsg_instantly("+919610033622","HI I Am Mukesh How are you 1",10,True,5)
#pwk.sendwhatmsg_instantly("+917383444121","HI I Am Mukesh K",10)


# time.sleep(4)
# count = 0
# while count <=5:
#     gui.typewrite("I love you "+str(count))
#     gui.press("enter")
#     count=count+1

print(emoji.emojize("I love reading books:books:"))
print(emoji.emojize("Some people have a very sensitive heart:red_heart: , please be kind with them.:hibiscus:"))
print(emoji.emojize(":grinning_face_with_big_eyes:"))
print(emoji.emojize(":winking_face_with_tongue:"))
print(emoji.emojize(":zipper-mouth_face:"))

import regex as re

# Text from which you want to extract emojis
text = 'We 😊 want 😅 to 😏 extract 😁 these 😀 emojis '

# Using regular expression to find and extract all emojis from the text
emojis = re.findall(r'[^\w\⁠s,. ]', text)
print(emojis)