import pandas as pd
import streamlit as st
#from datetime import datetime
import plotly.graph_objects as go
from jugaad_data.nse import *
import pandas_ta as pta
import altair as alt
import matplotlib.pyplot as plt
import mplfinance as mpf
from five_paisa1 import *
import datetime 

from collections import namedtuple
import pandas_ta as pta
#from finta import TA
# import talib
import pandas as pd
import copy
import numpy as np
import xlwings as xw
from datetime import datetime,timedelta
from numpy import log as nplog
from numpy import NaN as npNaN
from pandas import DataFrame, Series
from pandas_ta.overlap import ema, hl2
from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
from io import BytesIO
import os
import sys
from zipfile import ZipFile
import requests
import itertools
import math 
from telethon.sync import TelegramClient
#from notifypy import Notify
#from plyer import notification
import inspect
import time
from five_paisa1 import *
import threading

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

from_date = date(2024, 3, 1)
to_date = date(2024, 3, 21)

username = "haresh"
username1 = str(username)
client = credentials(username1)

All = ['20MICRONS', '21STCENMGM', '3IINFOTECH', '3MINDIA', '3PLAND', '5PAISA',
       '63MOONS', 'A2ZINFRA', 'AAATECH', 'AAKASH', 'AARON', 'AARTIDRUGS', 'AARTIIND',
       'AARTISURF', 'AARVEEDEN', 'AARVI', 'AAVAS', 'ABAN', 'ABB', 'ABBOTINDIA', 'ABCAPITAL',
       'ABFRL', 'ABINFRA', 'ABMINTLTD', 'ABSLBANETF', 'ABSLNN50ET', 'ACC', 'ACCELYA', 'ACCORD',
       'ACCURACY', 'ACE', 'ACRYSIL', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER',
       'ADANITRANS', 'ADFFOODS', 'ADL', 'ADORWELD', 'ADROITINFO', 'ADSL', 'ADVANIHOTR',
       'ADVENZYMES', 'AEGISCHEM', 'AFFLE', 'AGARIND', 'AGCNET', 'AGRITECH', 'AGROPHOS',
       'AHLADA', 'AHLEAST', 'AHLUCONT', 'AHLWEST', 'AIAENG', 'AIRAN', 'AIROLAM', 'AISL',
       'AJANTPHARM', 'AJMERA', 'AJOONI', 'AKASH', 'AKG', 'AKSHARCHEM', 'AKSHOPTFBR',
       'AKZOINDIA', 'ALANKIT', 'ALBERTDAVD', 'ALEMBICLTD', 'ALICON', 'ALKALI', 'ALKEM',
       'ALKYLAMINE', 'ALLCARGO', 'ALLSEC', 'ALMONDZ', 'ALOKINDS', 'ALPA', 'ALPHAGEO',
       'ALPSINDUS', 'AMARAJABAT', 'AMBANIORG', 'AMBER', 'AMBICAAGAR', 'AMBIKCO', 'AMBUJACEM',
       'AMDIND', 'AMJLAND', 'AMRUTANJAN', 'ANANTRAJ', 'ANDHRACEMT', 'ANDHRAPAP', 'ANDHRSUGAR',
       'ANGELBRKG', 'ANIKINDS', 'ANKITMETAL', 'ANMOL', 'ANSALAPI', 'ANSALHSG', 'ANUP', 'ANURAS',
       'APARINDS', 'APCL', 'APCOTEXIND', 'APEX', 'APLAPOLLO', 'APLLTD', 'APOLLO', 'APOLLOHOSP',
       'APOLLOPIPE', 'APOLLOTYRE', 'APOLSINHOT', 'APTECHT', 'ARCHIDPLY', 'ARCHIES', 'ARENTERP',
       'ARIES', 'ARIHANT', 'ARIHANTSUP', 'ARMANFIN', 'AROGRANITE', 'ARROWGREEN', 'ARSHIYA',
       'ARSSINFRA', 'ARTEMISMED', 'ARVEE', 'ARVIND', 'ARVINDFASN', 'ARVSMART', 'ASAHIINDIA',
       'ASAHISONG', 'ASAL', 'ASALCBR', 'ASHAPURMIN', 'ASHIANA', 'ASHIMASYN', 'ASHOKA', 'ASHOKLEY',
       'ASIANHOTNR', 'ASIANPAINT', 'ASIANTILES', 'ASPINWALL', 'ASTEC', 'ASTERDM', 'ASTRAL',
       'ASTRAMICRO', 'ASTRAZEN', 'ASTRON', 'ATALREAL', 'ATFL', 'ATGL', 'ATLANTA', 'ATUL', 'ATULAUTO',
       'AUBANK', 'AURDIS', 'AURIONPRO', 'AUROPHARMA', 'AUSOMENT', 'AUTOAXLES', 'AUTOIND', 'AVADHSUGAR',
       'AVANTIFEED', 'AVG', 'AVTNPL', 'AWHCL', 'AXISBANK', 'AXISBNKETF', 'AXISBPSETF', 'AXISCADES',
       'AXISGOLD', 'AXISHCETF', 'AXISNIFTY', 'AXISTECETF', 'AYMSYNTEX', 'BAFNAPH', 'BAGFILMS',
       'BAJAJ-AUTO', 'BAJAJCON', 'BAJAJELEC', 'BAJAJFINSV', 'BAJAJHIND', 'BAJAJHLDNG', 'BAJFINANCE',
       'BALAJITELE', 'BALAMINES', 'BALAXI', 'BALKRISHNA', 'BALKRISIND', 'BALLARPUR', 'BALMLAWRIE',
       'BALPHARMA', 'BALRAMCHIN', 'BANARBEADS', 'BANARISUG', 'BANCOINDIA', 'BANDHANBNK', 'BANG',
       'BANKA', 'BANKBARODA', 'BANKBEES', 'BANKINDIA', 'BANSWRAS', 'BARBEQUE', 'BARTRONICS', 'BASF',
       'BASML', 'BATAINDIA', 'BAYERCROP', 'BBL', 'BBTC', 'BBTCL', 'BCG', 'BCLIND', 'BCONCEPTS', 'BCP', 'BDL',
       'BEARDSELL', 'BECTORFOOD', 'BEDMUTHA', 'BEL', 'BEML', 'BEPL', 'BERGEPAINT', 'BESTAGRO', 'BETA', 'BFINVEST',
       'BFUTILITIE', 'BGRENERGY', 'BHAGERIA', 'BHAGYANGR', 'BHAGYAPROP', 'BHANDARI', 'BHARATFORG', 'BHARATGEAR',
       'BHARATRAS', 'BHARATWIRE', 'BHARTIARTL', 'BHEL', 'BIGBLOC', 'BIL', 'BINDALAGRO', 'BIOCON', 'BIOFILCHEM',
       'BIRLACABLE', 'BIRLACORPN', 'BIRLAMONEY', 'BIRLATYRE', 'BKMINDST', 'BLBLIMITED', 'BLISSGVS', 'BLKASHYAP', 'BLS',
       'BLUEDART', 'BLUESTARCO', 'BODALCHEM', 'BOHRA', 'BOMDYEING', 'BOROLTD', 'BORORENEW', 'BOSCHLTD', 'BPCL', 'BPL',
       'BRFL', 'BRIGADE', 'BRIGHT', 'BRITANNIA', 'BRNL', 'BROOKS', 'BSE', 'BSELINFRA', 'BSHSL', 'BSL', 'BSLGOLDETF',
       'BSLNIFTY', 'BSOFT', 'BURGERKING', 'BUTTERFLY', 'BVCL', 'BYKE', 'CADILAHC', 'CALSOFT', 'CAMLINFINE', 'CAMS',
       'CANBK', 'CANDC', 'CANFINHOME', 'CANTABIL', 'CAPACITE', 'CAPLIPOINT', 'CAPTRUST', 'CARBORUNIV', 'CAREERP',
       'CARERATING', 'CASTROLIND', 'CCCL', 'CCHHL', 'CCL', 'CDSL', 'CEATLTD', 'CEBBCO', 'CELEBRITY', 'CENTENKA',
       'CENTEXT', 'CENTRALBK', 'CENTRUM', 'CENTUM', 'CENTURYPLY', 'CENTURYTEX', 'CERA', 'CEREBRAINT', 'CESC', 'CGCL',
       'CGPOWER', 'CHALET', 'CHAMBLFERT', 'CHEMBOND', 'CHEMCON', 'CHEMFAB', 'CHENNPETRO', 'CHOLAFIN', 'CHOLAHLDNG',
       'CIGNITITEC', 'CINELINE', 'CINEVISTA', 'CIPLA', 'CLEDUCATE', 'CLNINDIA', 'CLSEL', 'CMICABLES', 'CMMIPL',
       'COALINDIA', 'COCHINSHIP', 'COFFEEDAY', 'COFORGE', 'COLPAL', 'COMPINFO', 'COMPUSOFT', 'CONCOR', 'CONFIPET',
       'CONSOFINVT', 'CONTI', 'CONTROLPR', 'CORALFINAC', 'CORDSCABLE', 'COROMANDEL', 'COSMOFILMS', 'COUNCODOS',
       'COX&KINGS', 'CPSEETF', 'CRAFTSMAN', 'CREATIVE', 'CREATIVEYE', 'CREDITACC', 'CREST', 'CRISIL', 'CROMPTON',
       'CROWN', 'CSBBANK', 'CTE', 'CUB', 'CUBEXTUB', 'CUMMINSIND', 'CUPID', 'CYBERMEDIA', 'CYBERTECH', 'CYIENT',
       'DAAWAT', 'DABUR', 'DALALSTCOM', 'DALBHARAT', 'DALMIASUG', 'DAMODARIND', 'DANGEE', 'DATAMATICS', 'DBCORP', 'DBL',
       'DBREALTY', 'DBSTOCKBRO', 'DCAL', 'DCBBANK', 'DCM', 'DCMFINSERV', 'DCMNVL', 'DCMSHRIRAM', 'DCW', 'DECCANCE',
       'DEEPAKFERT', 'DEEPAKNTR', 'DEEPENR', 'DEEPINDS', 'DELTACORP', 'DELTAMAGNT', 'DEN', 'DENORA', 'DFMFOODS',
       'DGCONTENT', 'DHAMPURSUG', 'DHANBANK', 'DHANI', 'DHANUKA', 'DHARSUGAR', 'DHFL', 'DHUNINV', 'DIAMONDYD',
       'DIAPOWER', 'DICIND', 'DIGISPICE', 'DISHTV', 'DIVISLAB', 'DIXON', 'DLF', 'DLINKINDIA', 'DMART', 'DNAMEDIA',
       'DOLAT', 'DOLLAR', 'DONEAR', 'DPABHUSHAN', 'DPSCLTD', 'DPWIRES', 'DRCSYSTEMS', 'DREDGECORP', 'DRREDDY', 'DSSL',
       'DTIL', 'DUCON', 'DVL', 'DWARKESH', 'DYNAMATECH', 'DYNPRO', 'E2E', 'EASEMYTRIP', 'EASTSILK', 'EASUNREYRL',
       'EBANK', 'EBBETF0423', 'EBBETF0425', 'EBBETF0430', 'EBBETF0431', 'EBIXFOREX', 'ECLERX', 'EDELWEISS', 'EDUCOMP',
       'EICHERMOT', 'EIDPARRY', 'EIFFL', 'EIHAHOTELS', 'EIHOTEL', 'EIMCOELECO', 'EKC', 'ELECON', 'ELECTCAST',
       'ELECTHERM', 'ELGIEQUIP', 'ELGIRUBCO', 'EMAMILTD', 'EMAMIPAP', 'EMAMIREAL', 'EMCO', 'EMKAY', 'EMKAYTOOLS',
       'EMMBI', 'ENDURANCE', 'ENERGYDEV', 'ENGINERSIN', 'ENIL', 'EPL', 'EQ30', 'EQUITAS', 'EQUITASBNK', 'ERIS',
       'EROSMEDIA', 'ESABINDIA', 'ESCORTS', 'ESSARSHPNG', 'ESTER', 'EUROTEXIND', 'EVEREADY', 'EVERESTIND', 'EXCEL',
       'EXCELINDUS', 'EXIDEIND', 'EXPLEOSOL', 'FACT', 'FAIRCHEMOR', 'FCL', 'FCONSUMER', 'FCSSOFT', 'FDC', 'FEDERALBNK',
       'FEL', 'FELDVR', 'FELIX', 'FIEMIND', 'FILATEX', 'FINCABLES', 'FINEORG', 'FINPIPE', 'FLEXITUFF', 'FLFL',
       'FLUOROCHEM', 'FMGOETZE', 'FMNL', 'FOCUS', 'FORCEMOT', 'FORTIS', 'FOSECOIND', 'FRETAIL', 'FSC', 'FSL', 'G5',
       'GABRIEL', 'GAEL', 'GAIL', 'GAL', 'GALAXYSURF', 'GALLANTT', 'GALLISPAT', 'GAMMNINFRA', 'GANDHITUBE', 'GANECOS',
       'GANESHHOUC', 'GANGAFORGE', 'GANGESSECU', 'GARFIBRES', 'GATI', 'GAYAHWS', 'GAYAPROJ', 'GDL', 'GEECEE',
       'GEEKAYWIRE', 'GENCON', 'GENESYS', 'GENUSPAPER', 'GENUSPOWER', 'GEOJITFSL', 'GEPIL', 'GESHIP', 'GET&D',
       'GFLLIMITED', 'GFSTEELS', 'GHCL', 'GICHSGFIN', 'GICRE', 'GILLANDERS', 'GILLETTE', 'GINNIFILA', 'GIPCL',
       'GKWLIMITED', 'GLAND', 'GLAXO', 'GLENMARK', 'GLFL', 'GLOBAL', 'GLOBALVECT', 'GLOBE', 'GLOBUSSPR', 'GMBREW',
       'GMDCLTD', 'GMMPFAUDLR', 'GMRINFRA', 'GNA', 'GNFC', 'GOACARBON', 'GOCLCORP', 'GODFRYPHLP', 'GODHA', 'GODREJAGRO',
       'GODREJCP', 'GODREJIND', 'GODREJPROP', 'GOENKA', 'GOKEX', 'GOKUL', 'GOKULAGRO', 'GOLDBEES', 'GOLDENTOBC',
       'GOLDIAM', 'GOLDSHARE', 'GOLDTECH', 'GOODLUCK', 'GOODYEAR', 'GPIL', 'GPPL', 'GPTINFRA', 'GRANULES', 'GRAPHITE',
       'GRASIM', 'GRAVITA', 'GREAVESCOT', 'GREENLAM', 'GREENPANEL', 'GREENPLY', 'GREENPOWER', 'GRINDWELL', 'GROBTEA',
       'GRPLTD', 'GRSE', 'GSCLCEMENT', 'GSFC', 'GSPL', 'GSS', 'GTL', 'GTLINFRA', 'GTNTEX', 'GTPL', 'GUFICBIO',
       'GUJALKALI', 'GUJAPOLLO', 'GUJGASLTD', 'GUJRAFFIA', 'GULFOILLUB', 'GULFPETRO', 'GULPOLY', 'HAL', 'HAPPSTMNDS',
       'HARRMALAYA', 'HATHWAY', 'HATSUN', 'HAVELLS', 'HAVISHA', 'HBANKETF', 'HBLPOWER', 'HBSL', 'HCC', 'HCG',
       'HCL-INSYS', 'HCLTECH', 'HDFC', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HDFCMFGETF', 'HDFCNIFETF', 'HDFCSENETF',
       'HDIL', 'HEG', 'HEIDELBERG', 'HEMIPROP', 'HERANBA', 'HERCULES', 'HERITGFOOD', 'HEROMOTOCO', 'HESTERBIO',
       'HEXATRADEX', 'HFCL', 'HGINFRA', 'HGS', 'HIKAL', 'HIL', 'HILTON', 'HIMATSEIDE', 'HINDALCO', 'HINDCOMPOS',
       'HINDCOPPER', 'HINDMOTORS', 'HINDNATGLS', 'HINDOILEXP', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'HIRECT',
       'HISARMETAL', 'HITECH', 'HITECHCORP', 'HITECHGEAR', 'HLEGLAS', 'HLVLTD', 'HMT', 'HMVL', 'HNDFDS', 'HNGSNGBEES',
       'HOMEFIRST', 'HONAUT', 'HONDAPOWER', 'HOTELRUGBY', 'HOVS', 'HPIL', 'HPL', 'HSCL', 'HSIL', 'HTMEDIA', 'HUBTOWN',
       'HUDCO', 'HUHTAMAKI', 'HUSYSLTD', 'IBMFNIFTY', 'IBREALEST', 'IBULHSGFIN', 'ICEMAKE', 'ICICI500', 'ICICIALPLV',
       'ICICIB22', 'ICICIBANK', 'ICICIBANKN', 'ICICIBANKP', 'ICICIGI', 'ICICIGOLD', 'ICICILIQ', 'ICICILOVOL',
       'ICICIM150', 'ICICIMCAP', 'ICICINF100', 'ICICINIFTY', 'ICICINV20', 'ICICINXT50', 'ICICIPHARM', 'ICICIPRULI',
       'ICICISENSX', 'ICICITECH', 'ICIL', 'ICRA', 'IDBI', 'IDBIGOLD', 'IDEA', 'IDFC', 'IDFCFIRSTB', 'IDFNIFTYET', 'IEX',
       'IFBAGRO', 'IFBIND', 'IFCI', 'IFGLEXPOR', 'IGARASHI', 'IGL', 'IGPL', 'IIFL', 'IIFLSEC', 'IIFLWAM', 'IITL',
       'IL&FSENGG', 'IL&FSTRANS', 'IMAGICAA', 'IMFA', 'IMPAL', 'IMPEXFERRO', 'INCREDIBLE', 'INDBANK', 'INDHOTEL',
       'INDIACEM', 'INDIAGLYCO', 'INDIAMART', 'INDIANB', 'INDIANCARD', 'INDIANHUME', 'INDIGO', 'INDIGOPNTS',
       'INDLMETER', 'INDNIPPON', 'INDOCO', 'INDORAMA', 'INDOSOLAR', 'INDOSTAR', 'INDOTECH', 'INDOTHAI', 'INDOWIND',
       'INDRAMEDCO', 'INDSWFTLAB', 'INDTERRAIN', 'INDUSINDBK', 'INDUSTOWER', 'INEOSSTYRO', 'INFIBEAM', 'INFOBEAN',
       'INFOMEDIA', 'INFRABEES', 'INFY', 'INGERRAND', 'INNOVANA', 'INNOVATIVE', 'INOXLEISUR', 'INOXWIND', 'INSECTICID',
       'INSPIRISYS', 'INTELLECT', 'INTENTECH', 'INVENTURE', 'IOB', 'IOC', 'IOLCP', 'IPCALAB', 'IRB', 'IRCON', 'IRCTC',
       'IRFC', 'IRISDOREME', 'ISEC', 'ISFT', 'ISGEC', 'ISMTLTD', 'ITC', 'ITDC', 'ITDCEM', 'ITI', 'IVC', 'IVP',
       'IVZINGOLD', 'IVZINNIFTY', 'IZMO', 'J&KBANK', 'JAGRAN', 'JAGSNPHARM', 'JAIBALAJI', 'JAICORPLTD', 'JAINSTUDIO',
       'JAMNAAUTO', 'JASH', 'JAYAGROGN', 'JAYBARMARU', 'JAYNECOIND', 'JAYSREETEA', 'JBCHEPHARM', 'JBFIND', 'JBMA',
       'JCHAC', 'JETAIRWAYS', 'JETFREIGHT', 'JETKNIT', 'JHS', 'JIKIND', 'JINDALPHOT', 'JINDALPOLY', 'JINDALSAW',
       'JINDALSTEL', 'JINDRILL', 'JINDWORLD', 'JISLDVREQS', 'JISLJALEQS', 'JITFINFRA', 'JIYAECO', 'JKCEMENT', 'JKIL',
       'JKLAKSHMI', 'JKPAPER', 'JKTYRE', 'JMA', 'JMCPROJECT', 'JMFINANCIL', 'JMTAUTOLTD', 'JOCIL', 'JPASSOCIAT',
       'JPINFRATEC', 'JPPOWER', 'JSL', 'JSLHISAR', 'JSWENERGY', 'JSWHL', 'JSWISPL', 'JSWSTEEL', 'JTEKTINDIA',
       'JUBLFOOD', 'JUBLINDS', 'JUBLINGREA', 'JUBLPHARMA', 'JUMPNET', 'JUNIORBEES', 'JUSTDIAL', 'JYOTHYLAB',
       'JYOTISTRUC', 'KABRAEXTRU', 'KAJARIACER', 'KAKATCEM', 'KALPATPOWR', 'KALYANIFRG', 'KALYANKJIL', 'KAMATHOTEL',
       'KAMDHENU', 'KANANIIND', 'KANORICHEM', 'KANPRPLA', 'KANSAINER', 'KAPSTON', 'KARDA', 'KARMAENG', 'KARURVYSYA',
       'KAUSHALYA', 'KAYA', 'KCP', 'KCPSUGIND', 'KDDL', 'KEC', 'KECL', 'KEERTI', 'KEI', 'KELLTONTEC', 'KENNAMET',
       'KERNEX', 'KESORAMIND', 'KEYFINSERV', 'KHADIM', 'KHAICHEM', 'KHANDSE', 'KICL', 'KILITCH', 'KINGFA', 'KIOCL',
       'KIRIINDUS', 'KIRLFER', 'KIRLOSBROS', 'KIRLOSENG', 'KIRLOSIND', 'KITEX', 'KKCL', 'KKVAPOW', 'KMSUGAR', 'KNRCON',
       'KOKUYOCMLN', 'KOLTEPATIL', 'KOPRAN', 'KOTAKBANK', 'KOTAKBKETF', 'KOTAKGOLD', 'KOTAKIT', 'KOTAKNIFTY',
       'KOTAKNV20', 'KOTAKPSUBK', 'KOTARISUG', 'KOTHARIPET', 'KOTHARIPRO', 'KPITTECH', 'KPRMILL', 'KRBL', 'KREBSBIO',
       'KRIDHANINF', 'KRISHANA', 'KSB', 'KSCL', 'KSHITIJPOL', 'KSL', 'KSOLVES', 'KTKBANK', 'KUANTUM', 'L&TFH', 'LAGNAM',
       'LAKPRE', 'LALPATHLAB', 'LAMBODHARA', 'LAOPALA', 'LASA', 'LAURUSLABS', 'LAXMICOT', 'LAXMIMACH', 'LCCINFOTEC',
       'LEMONTREE', 'LEXUS', 'LFIC', 'LGBBROSLTD', 'LGBFORGE', 'LIBAS', 'LIBERTSHOE', 'LICHSGFIN', 'LICNETFGSC',
       'LICNETFN50', 'LICNETFSEN', 'LICNFNHGP', 'LIKHITHA', 'LINCOLN', 'LINCPEN', 'LINDEINDIA', 'LIQUIDBEES',
       'LIQUIDETF', 'LODHA', 'LOKESHMACH', 'LOTUSEYE', 'LOVABLE', 'LPDC', 'LSIL', 'LT', 'LTI', 'LTTS', 'LUMAXIND',
       'LUMAXTECH', 'LUPIN', 'LUXIND', 'LXCHEM', 'LYKALABS', 'LYPSAGEMS', 'M&M', 'M&MFIN', 'M100', 'M50', 'MAANALU',
       'MACPOWER', 'MADHAV', 'MADHUCON', 'MADRASFERT', 'MAESGETF', 'MAFANG', 'MAGADSUGAR', 'MAGMA', 'MAGNUM',
       'MAHABANK', 'MAHAPEXLTD', 'MAHASTEEL', 'MAHEPC', 'MAHESHWARI', 'MAHICKRA', 'MAHINDCIE', 'MAHLIFE', 'MAHLOG',
       'MAHSCOOTER', 'MAHSEAMLES', 'MAITHANALL', 'MAJESCO', 'MALUPAPER', 'MAN50ETF', 'MANAKALUCO', 'MANAKCOAT',
       'MANAKSIA', 'MANAKSTEEL', 'MANALIPETC', 'MANAPPURAM', 'MANGALAM', 'MANGCHEFER', 'MANGLMCEM', 'MANGTIMBER',
       'MANINDS', 'MANINFRA', 'MANUGRAPH', 'MANXT50', 'MARALOVER', 'MARATHON', 'MARICO', 'MARINE', 'MARKSANS',
       'MARSHALL', 'MARUTI', 'MASFIN', 'MASKINVEST', 'MASTEK', 'MATRIMONY', 'MAWANASUG', 'MAXHEALTH', 'MAXIND',
       'MAXVIL', 'MAYURUNIQ', 'MAZDA', 'MAZDOCK', 'MBAPL', 'MBECL', 'MBLINFRA', 'MCDHOLDING', 'MCDOWELL-N', 'MCL',
       'MCLEODRUSS', 'MCX', 'MEGASOFT', 'MELSTAR', 'MENONBE', 'MEP', 'MERCATOR', 'METALFORGE', 'METROPOLIS', 'MFSL',
       'MGEL', 'MGL', 'MHHL', 'MHRIL', 'MIDHANI', 'MINDACORP', 'MINDAIND', 'MINDTECK', 'MINDTREE', 'MIRCELECTR',
       'MIRZAINT', 'MITTAL', 'MMFL', 'MMP', 'MMTC', 'MODIRUBBER', 'MODISNME', 'MOHITIND', 'MOHOTAIND', 'MOIL', 'MOKSH',
       'MOLDTECH', 'MOLDTKPAC', 'MONTECARLO', 'MORARJEE', 'MOREPENLAB', 'MOTHERSUMI', 'MOTILALOFS', 'MOTOGENFIN',
       'MPHASIS', 'MPSLTD', 'MRF', 'MRO-TEK', 'MRPL', 'MSPL', 'MSTCLTD', 'MTARTECH', 'MTEDUCARE', 'MTNL', 'MUKANDLTD',
       'MUKTAARTS', 'MUNJALAU', 'MUNJALSHOW', 'MURUDCERA', 'MUTHOOTCAP', 'MUTHOOTFIN', 'N100', 'NACLIND', 'NAGAFERT',
       'NAGREEKCAP', 'NAGREEKEXP', 'NAHARCAP', 'NAHARINDUS', 'NAHARPOLY', 'NAHARSPING', 'NAM-INDIA', 'NANDANI',
       'NATCOPHARM', 'NATHBIOGEN', 'NATIONALUM', 'NAUKRI', 'NAVINFLUOR', 'NAVKARCORP', 'NAVNETEDUL', 'NAZARA', 'NBCC',
       'NBIFIN', 'NBVENTURES', 'NCC', 'NCLIND', 'NCPSESDL24', 'NDGL', 'NDL', 'NDRAUTO', 'NDTV', 'NECCLTD', 'NECLIFE',
       'NELCAST', 'NELCO', 'NEOGEN', 'NESCO', 'NESTLEIND', 'NETF', 'NETFCONSUM', 'NETFDIVOPP', 'NETFGILT5Y', 'NETFIT',
       'NETFLTGILT', 'NETFMID150', 'NETFNIF100', 'NETFNV20', 'NETFSDL26', 'NETWORK18', 'NEULANDLAB', 'NEWGEN',
       'NEXTMEDIA', 'NFL', 'NH', 'NHPC', 'NIACL', 'NIBL', 'NIFTYBEES', 'NIITLTD', 'NILAINFRA', 'NILASPACES', 'NILKAMAL',
       'NIPPOBATRY', 'NIRAJ', 'NITCO', 'NITINFIRE', 'NITINSPIN', 'NITIRAJ', 'NKIND', 'NLCINDIA', 'NMDC', 'NOCIL',
       'NOIDATOLL', 'NORBTEAEXP', 'NOVARTIND', 'NPBET', 'NRAIL', 'NRBBEARING', 'NSIL', 'NTL', 'NTPC', 'NUCLEUS',
       'NURECA', 'NXTDIGITAL', 'OAL', 'OBEROIRLTY', 'OCCL', 'OFSS', 'OIL', 'OLECTRA', 'OMAXAUTO', 'OMAXE', 'OMINFRAL',
       'ONELIFECAP', 'ONEPOINT', 'ONGC', 'ONMOBILE', 'ONWARDTEC', 'OPTIEMUS', 'OPTOCIRCUI', 'ORBTEXP', 'ORCHPHARMA',
       'ORICONENT', 'ORIENTABRA', 'ORIENTALTL', 'ORIENTBELL', 'ORIENTCEM', 'ORIENTELEC', 'ORIENTHOT', 'ORIENTLTD',
       'ORIENTPPR', 'ORIENTREF', 'ORISSAMINE', 'ORTEL', 'ORTINLAB', 'OSIAHYPER', 'OSWALAGRO', 'PAEL', 'PAGEIND',
       'PAISALO', 'PALASHSECU', 'PALREDTEC', 'PANACEABIO', 'PANACHE', 'PANAMAPET', 'PANSARI', 'PAR', 'PARACABLES',
       'PARAGMILK', 'PARSVNATH', 'PARTYCRUS', 'PATELENG', 'PATINTLOG', 'PATSPINLTD', 'PAVNAIND', 'PBAINFRA',
       'PCJEWELLER', 'PDMJEPAPER', 'PDSMFL', 'PEARLPOLY', 'PEL', 'PENIND', 'PENINLAND', 'PENTAGOLD', 'PERSISTENT',
       'PETRONET', 'PFC', 'PFIZER', 'PFOCUS', 'PFS', 'PGEL', 'PGHH', 'PGHL', 'PGIL', 'PHILIPCARB', 'PHOENIXLTD',
       'PIDILITIND', 'PIIND', 'PILANIINVS', 'PILITA', 'PIONDIST', 'PIONEEREMB', 'PITTIENG', 'PKTEA', 'PLASTIBLEN',
       'PNB', 'PNBGILTS', 'PNBHOUSING', 'PNC', 'PNCINFRA', 'PODDARHOUS', 'PODDARMENT', 'POKARNA', 'POLYCAB', 'POLYMED',
       'POLYPLEX', 'PONNIERODE', 'POWERGRID', 'POWERINDIA', 'POWERMECH', 'PPAP', 'PPL', 'PRAENG', 'PRAJIND', 'PRAKASH',
       'PRAKASHSTL', 'PRAXIS', 'PRECAM', 'PRECOT', 'PRECWIRE', 'PREMEXPLN', 'PREMIER', 'PREMIERPOL', 'PRESSMN',
       'PRESTIGE', 'PRICOLLTD', 'PRIMESECU', 'PRINCEPIPE', 'PRIVISCL', 'PROINDIA', 'PROLIFE', 'PROZONINTU',
       'PRSMJOHNSN', 'PSB', 'PSPPROJECT', 'PSUBNKBEES', 'PTC', 'PTL', 'PULZ', 'PUNJABCHEM', 'PUNJLLOYD', 'PURVA', 'PVR',
       'QGOLDHALF', 'QNIFTY', 'QUESS', 'QUICKHEAL', 'RADAAN', 'RADICO', 'RADIOCITY', 'RAILTEL', 'RAIN', 'RAJESHEXPO',
       'RAJMET', 'RAJRATAN', 'RAJRAYON', 'RAJSREESUG', 'RAJTV', 'RALLIS', 'RAMANEWS', 'RAMASTEEL', 'RAMCOCEM',
       'RAMCOIND', 'RAMCOSYS', 'RAMKY', 'RAMSARUP', 'RANASUG', 'RANEENGINE', 'RANEHOLDIN', 'RATNAMANI', 'RAYMOND',
       'RBL', 'RBLBANK', 'RCF', 'RCOM', 'RECLTD', 'REDINGTON', 'REFEX', 'RELAXO', 'RELCAPITAL', 'RELIANCE', 'RELIGARE',
       'RELINFRA', 'REMSONSIND', 'RENUKA', 'REPCOHOME', 'REPL', 'REPRO', 'RESPONIND', 'REVATHI', 'RGL', 'RHFL',
       'RICOAUTO', 'RIIL', 'RITES', 'RKDL', 'RKEC', 'RKFORGE', 'RMCL', 'RMDRIP', 'RML', 'RNAVAL', 'ROHLTD', 'ROLLT',
       'ROLTA', 'ROML', 'ROSSARI', 'ROSSELLIND', 'ROUTE', 'RPGLIFE', 'RPOWER', 'RPPINFRA', 'RPPL', 'RPSGVENT',
       'RSSOFTWARE', 'RSWM', 'RSYSTEMS', 'RTNINDIA', 'RTNPOWER', 'RUBYMILLS', 'RUCHI', 'RUCHINFRA', 'RUCHIRA', 'RUPA',
       'RUSHIL', 'RVHL', 'RVNL', 'S&SPOWER', 'SABEVENTS', 'SABTN', 'SADBHAV', 'SADBHIN', 'SAFARI', 'SAGARDEEP',
       'SAGCEM', 'SAIL', 'SAKAR', 'SAKHTISUG', 'SAKSOFT', 'SAKUMA', 'SALASAR', 'SALONA', 'SALSTEEL', 'SALZERELEC',
       'SAMBHAAV', 'SANCO', 'SANDESH', 'SANDHAR', 'SANGAMIND', 'SANGHIIND', 'SANGHVIMOV', 'SANGINITA', 'SANOFI',
       'SANWARIA', 'SARDAEN', 'SAREGAMA', 'SARLAPOLY', 'SARVESHWAR', 'SASKEN', 'SASTASUNDR', 'SATIA', 'SATIN',
       'SBICARD', 'SBIETFIT', 'SBIETFPB', 'SBIETFQLTY', 'SBILIFE', 'SBIN', 'SCAPDVR', 'SCHAEFFLER', 'SCHAND',
       'SCHNEIDER', 'SCI', 'SDBL', 'SEAMECLTD', 'SECL', 'SECURCRED', 'SECURKLOUD', 'SELAN', 'SEPOWER', 'SEQUENT',
       'SERVOTECH', 'SESHAPAPER', 'SETCO', 'SETF10GILT', 'SETFGOLD', 'SETFNIF50', 'SETFNIFBK', 'SETFNN50', 'SETUINFRA',
       'SEYAIND', 'SFL', 'SGL', 'SHAKTIPUMP', 'SHALBY', 'SHALPAINTS', 'SHANKARA', 'SHANTIGEAR', 'SHARDACROP',
       'SHARDAMOTR', 'SHAREINDIA', 'SHARIABEES', 'SHEMAROO', 'SHIL', 'SHILPAMED', 'SHIVAMAUTO', 'SHIVAMILLS',
       'SHIVATEX', 'SHK', 'SHOPERSTOP', 'SHRADHA', 'SHREDIGCEM', 'SHREECEM', 'SHREEPUSHK', 'SHREERAMA', 'SHRENIK',
       'SHREYANIND', 'SHREYAS', 'SHRIPISTON', 'SHRIRAMCIT', 'SHRIRAMEPC', 'SHUBHLAXMI', 'SHYAMCENT', 'SHYAMTEL',
       'SICAGEN', 'SICAL', 'SIEMENS', 'SIGIND', 'SIGMA', 'SIL', 'SILGO', 'SILINV', 'SILLYMONKS', 'SILVERTUC',
       'SIMBHALS', 'SIMPLEXINF', 'SINTERCOM', 'SINTEX', 'SIRCA', 'SIS', 'SITINET', 'SIYSIL', 'SJVN', 'SKFINDIA', 'SKIL',
       'SKIPPER', 'SKMEGGPROD', 'SKSTEXTILE', 'SMARTLINK', 'SMCGLOBAL', 'SMLISUZU', 'SMPL', 'SMSLIFE', 'SMSPHARMA',
       'SMVD', 'SNOWMAN', 'SOBHA', 'SOLARA', 'SOLARINDS', 'SOLEX', 'SOMANYCERA', 'SOMATEX', 'SOMICONVEY', 'SONAMCLOCK',
       'SONATSOFTW', 'SORILINFRA', 'SOTL', 'SOUTHBANK', 'SOUTHWEST', 'SPAL', 'SPANDANA', 'SPARC', 'SPECIALITY',
       'SPECTRUM', 'SPENCERS', 'SPENTEX', 'SPIC', 'SPICEJET', 'SPLIL', 'SPMLINFRA', 'SPTL', 'SREEL', 'SREINFRA', 'SRF',
       'SRHHYPOLTD', 'SRIPIPES', 'SRPL', 'SRTRANSFIN', 'SSWL', 'STAR', 'STARCEMENT', 'STARPAPER', 'STCINDIA',
       'STEELCITY', 'STEELXIND', 'STEL', 'STERTOOLS', 'STLTECH', 'STOVEKRAFT', 'SUBCAPCITY', 'SUBEXLTD', 'SUBROS',
       'SUDARSCHEM', 'SUMEETINDS', 'SUMICHEM', 'SUMIT', 'SUMMITSEC', 'SUNCLAYLTD', 'SUNDARAM', 'SUNDARMFIN',
       'SUNDARMHLD', 'SUNDRMBRAK', 'SUNDRMFAST', 'SUNFLAG', 'SUNPHARMA', 'SUNTECK', 'SUNTV', 'SUPERHOUSE', 'SUPERSPIN',
       'SUPPETRO', 'SUPRAJIT', 'SUPREMEENG', 'SUPREMEIND', 'SURANASOL', 'SURANAT&P', 'SURYALAXMI', 'SURYAROSNI',
       'SURYODAY', 'SUTLEJTEX', 'SUULD', 'SUVEN', 'SUVENPHAR', 'SUVIDHAA', 'SUZLON', 'SWANENERGY', 'SWARAJENG',
       'SWELECTES', 'SWSOLAR', 'SYMPHONY', 'SYNCOM', 'SYNGENE', 'TAINWALCHM', 'TAJGVK', 'TAKE', 'TALBROAUTO', 'TANLA',
       'TANTIACONS', 'TARACHAND', 'TARAPUR', 'TARC', 'TARMAT', 'TASTYBITE', 'TATACHEM', 'TATACOFFEE', 'TATACOMM',
       'TATACONSUM', 'TATAELXSI', 'TATAINVEST', 'TATAMETALI', 'TATAMOTORS', 'TATAMTRDVR', 'TATAPOWER', 'TATASTEEL',
       'TATASTLBSL', 'TATASTLLP', 'TBZ', 'TCI', 'TCIDEVELOP', 'TCIEXP', 'TCIFINANCE', 'TCNSBRANDS', 'TCPLPACK', 'TCS',
       'TDPOWERSYS', 'TEAMLEASE', 'TECHIN', 'TECHM', 'TECHNOE', 'TEJASNET', 'TEMBO', 'TERASOFT', 'TEXINFRA',
       'TEXMOPIPES', 'TEXRAIL', 'TFCILTD', 'TFL', 'TGBHOTELS', 'THANGAMAYL', 'THEINVEST', 'THEJO', 'THEMISMED',
       'THERMAX', 'THOMASCOOK', 'THOMASCOTT', 'THYROCARE', 'TI', 'TIDEWATER', 'TIIL', 'TIINDIA', 'TIJARIA', 'TIL',
       'TIMESGTY', 'TIMETECHNO', 'TIMKEN', 'TINPLATE', 'TIPSINDLTD', 'TIRUMALCHM', 'TIRUPATIFL', 'TITAN', 'TMRVL',
       'TNPETRO', 'TNPL', 'TNTELE', 'TOKYOPLAST', 'TORNTPHARM', 'TORNTPOWER', 'TOTAL', 'TOUCHWOOD', 'TPLPLASTEH',
       'TREEHOUSE', 'TREJHARA', 'TRENT', 'TRF', 'TRIDENT', 'TRIGYN', 'TRIL', 'TRITURBINE', 'TRIVENI', 'TTKHLTCARE',
       'TTKPRESTIG', 'TTL', 'TTML', 'TV18BRDCST', 'TVSELECT', 'TVSMOTOR', 'TVSSRICHAK', 'TVTODAY', 'TVVISION', 'TWL',
       'UBL', 'UCALFUEL', 'UCL', 'UCOBANK', 'UFLEX', 'UFO', 'UGARSUGAR', 'UJAAS', 'UJJIVAN', 'UJJIVANSFB', 'ULTRACEMCO',
       'UMANGDAIRY', 'UMESLTD', 'UNICHEMLAB', 'UNIDT', 'UNIENTER', 'UNIONBANK', 'UNITECH', 'UNITEDPOLY', 'UNITEDTEA',
       'UNIVASTU', 'UNIVCABLES', 'UNIVPHOTO', 'UPL', 'URJA', 'USHAMART', 'UTIAMC', 'UTIBANKETF', 'UTINEXT50',
       'UTINIFTETF', 'UTISENSETF', 'UTISXN50', 'UTTAMSTL', 'UTTAMSUGAR', 'V2RETAIL', 'VADILALIND', 'VAIBHAVGBL',
       'VAISHALI', 'VAKRANGEE', 'VALIANTORG', 'VARDHACRLC', 'VARDMNPOLY', 'VARROC', 'VASA', 'VASCONEQ', 'VASWANI',
       'VBL', 'VCL', 'VEDL', 'VENKEYS', 'VENUSREM', 'VERTOZ', 'VESUVIUS', 'VETO', 'VGUARD', 'VHL', 'VICEROY',
       'VIDEOIND', 'VIDHIING', 'VIJIFIN', 'VIKASECO', 'VIKASLIFE', 'VIKASPROP', 'VIKASWSP', 'VIMTALABS', 'VINATIORGA',
       'VINDHYATEL', 'VINYLINDIA', 'VIPCLOTHNG', 'VIPIND', 'VIPULLTD', 'VISAKAIND', 'VISASTEEL', 'VISHAL', 'VISHNU',
       'VISHWARAJ', 'VIVIDHA', 'VIVIMEDLAB', 'VLSFINANCE', 'VMARCIND', 'VMART', 'VOLTAMP', 'VOLTAS', 'VRLLOG', 'VSSL',
       'VSTIND', 'VSTTILLERS', 'VTL', 'WABAG', 'WABCOINDIA', 'WALCHANNAG', 'WANBURY', 'WATERBASE', 'WEALTH',
       'WEBELSOLAR', 'WEIZMANIND', 'WELCORP', 'WELENT', 'WELINV', 'WELSPUNIND', 'WENDT', 'WESTLIFE', 'WEWIN', 'WFL',
       'WHEELS', 'WHIRLPOOL', 'WILLAMAGOR', 'WINDMACHIN', 'WIPL', 'WIPRO', 'WOCKPHARMA', 'WONDERLA', 'WORTH', 'WSI',
       'WSTCSTPAPR', 'XCHANGING', 'XELPMOC', 'XPROINDIA', 'YAARII', 'YESBANK', 'ZEEL', 'ZEELEARN', 'ZEEMEDIA',
       'ZENITHEXPO', 'ZENSARTECH', 'ZENTEC', 'ZODIACLOTH', 'ZODJRDMKJ', 'ZOTA', 'ZUARI', 'ZUARIGLOB', 'ZYDUSWELL'
       ]

CN100 = ['ABBOTINDIA', 'ACC', 'ADANIGREEN', 'ADANIPORTS', 'ADANITRANS', 'ALKEM', 'AMBUJACEM', 'ASIANPAINT',
         'AUROPHARMA', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJFINSV', 'BAJAJHLDNG', 'BAJFINANCE', 'BANDHANBNK', 'BANKBARODA',
         'BERGEPAINT', 'BHARTIARTL', 'BIOCON', 'BOSCHLTD', 'BPCL', 'BRITANNIA', 'CADILAHC', 'CIPLA', 'COALINDIA',
         'COLPAL', 'CONCOR', 'DABUR', 'DIVISLAB', 'DLF', 'DMART', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GICRE', 'GODREJCP',
         'GRASIM', 'HAVELLS', 'HCLTECH', 'HDFC', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO',
         'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'IGL', 'INDIGO', 'INDUSINDBK',
         'INDUSTOWER', 'INFY', 'IOC', 'ITC', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'LTI', 'LUPIN', 'M&M', 'MARICO', 'MARUTI',
         'MCDOWELL-N', 'MOTHERSUMI', 'MUTHOOTFIN', 'NAUKRI', 'NESTLEIND', 'NMDC', 'NTPC', 'OFSS', 'ONGC', 'PEL',
         'PETRONET', 'PFC', 'PGHH', 'PIDILITIND', 'PNB', 'POWERGRID', 'RELIANCE', 'SBICARD', 'SBILIFE', 'SBIN',
         'SHREECEM', 'SIEMENS', 'SUNPHARMA', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TCS', 'TECHM', 'TITAN',
         'TORNTPHARM', 'UBL', 'ULTRACEMCO', 'UPL', 'WIPRO'
         ]


def order_book_func(cred):
    try:
       ordbook = pd.DataFrame(cred.order_book())
       ordbook['Root'] = [x.split(' ')[-0] for x in ordbook['ScripName']]
       #ordbook[['Root']] = ordbook['ScripName'].str.split(' ',expand=True)
       #ordbook['Root'] = ordbook['ScripName'].tolist()#.str.split(" ")[0]
       #pos.range("r1").options(index=False).value = ordbook
        
    except Exception as e:
                print(e)

    try:
       if ordbook is not None:
            ordbook['Root'] = [x.split(' ')[-0] for x in ordbook['ScripName']]
            #ordbook['Root'] = ordbook['ScripName'].tolist()#.str.split(" ")[0]
            #print("Order Book not Empty")        
            ordbook1 = ordbook[ordbook['OrderStatus'] != "Rejected By 5P"]   
            ordbook1 = ordbook           
            Datetimeee = []
            for i in range(len(ordbook1)):
                datee = ordbook1['BrokerOrderTime'][i]
                timestamp = pd.to_datetime(datee[6:19], unit='ms')
                ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M')
                d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]))
                d2 = d1 + timedelta(hours = 5.5)
                Datetimeee.append(d2)
            ordbook1['Datetimeee'] = Datetimeee
            ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot','ExchOrderID','OrderStatus', 'OrderValidUpto','ScripName','Root','AtMarket']]
            ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
            #pos.range("a1").options(index=False).value = ordbook1
       else:
            print("Order Book Empty")
    except Exception as e:
                print(e)
    return ordbook1


buy_order = order_book_func(client)
buy_order_li = buy_order[(buy_order['BuySell'] == 'B') & (buy_order['OrderStatus'] == 'Fully Executed')]
print(buy_order_li)


start = datetime.time(9, 30, 0)
end = datetime.time(14, 45, 0)
current = datetime.datetime.now().time()
print(start, end, current)




if current > start and current < end:
    print("Time Not Over")
else:
    print("Time Over")



symbol = 999920000

#CE_df = client.historical_data('N', 'C', symbol, '5m', from_date,to_date)
#print(CE_df.head(5))

#start_time = 

# nse = NSELive()

# dates_list = stock_df(symbol="SBIN", from_date=from_date, to_date=to_date, series="EQ")
# dates_list = dates_list['DATE']
# print(dates_list)


# def bhavcopy(dates_list1):   
#     data_eq = pd.DataFrame()
#     for day in dates_list1:
#         print(day)
#         try:
#             dmyformat = datetime.strftime(day, '%d%m%Y')
#             url = 'https://archives.nseindia.com/products/content/sec_bhavdata_full_' + dmyformat + '.csv'
#             bhav_eq1 = pd.read_csv(url)
#             bhav_eq1.columns = bhav_eq1.columns.str.strip()
#             bhav_eq1 = bhav_eq1.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
#             bhav_eq1['DATE1'] = pd.to_datetime(bhav_eq1['DATE1'])
#             bhav_eq = bhav_eq1[bhav_eq1['SERIES'] == 'EQ']
#             bhav_eq['LAST_PRICE'] = bhav_eq['LAST_PRICE'].astype(float)
#             bhav_eq['DELIV_QTY'] = bhav_eq['DELIV_QTY'].astype(float)
#             bhav_eq['DELIV_PER'] = bhav_eq['DELIV_PER'].astype(float)
#             data_eq = pd.concat([bhav_eq, data_eq])
#         except Exception as e:
#             print(f'erroe {e} for {day}')
#     return data_eq

# data_eq = bhavcopy(dates_list)
# Symbol = "IDEA"
# data = data_eq[data_eq['SYMBOL'] == Symbol]

# print(data)
# # engulfing_pattern = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close']).replace(0, np.nan)
# # bull_engulf = engulfing_pattern.replace(-100, np.nan) / 100
# # bear_engulf = engulfing_pattern.replace(100, np.nan) / 100
# # print(bear_engulf)
# # deliv_data = [mpf.make_addplot(data['Deliv_per'], panel=2, mav=5),
# #                mpf.make_addplot(bull_engulf * data.Low * 0.97, type='scatter', marker='^', color='green'),
# #                mpf.make_addplot(-bear_engulf * data.High * 1.03, type='scatter', marker='v', color='red')]
# mpf.plot(data, addplot=deliv_data, type='candle', style='yahoo', volume=True)
# # data = ta.add_trend_ta(data,data['HIGH_PRICE'], data['LOW_PRICE'], data['CLOSE_PRICE'])
# #engulfing_pattern = pta.cdl_pattern(data['OPEN_PRICE'], data['HIGH_PRICE'], data['LOW_PRICE'], data['CLOSE_PRICE'],"engulfing")
# df_engulfing = data[data["bullish_engulfing"] == True]
# print(df_engulfing)


# # df = data_eq
# # # df = pd.read_csv('NSE_Bhavcopy.csv')
# # df['DATE'] = pd.to_datetime(df['DATE1'])

# # st.title('Stock Technical Analysis')
# # st.sidebar.title("Stock Technical Analysis")
# # select_type = st.sidebar.selectbox('Select Type', ['All', 'CN100'])
# # select = 'ITC'
# # if select_type == 'All':
# #     select = st.sidebar.selectbox('Select SYMBOL', All)
# # elif select_type == 'CN100':
# #     select = st.sidebar.selectbox('Select SYMBOL', CN100)

# # # Simple Moving average calculation
# # df_for_plot = df.loc[(df['SYMBOL'] == select) & (df['SERIES'] == 'EQ')]
# # df_for_plot['SMA44'] = df_for_plot['CLOSE_PRICE'].rolling(44).mean()
# # df_for_plot['SMA10'] = df_for_plot['CLOSE_PRICE'].rolling(10).mean()
# # df_for_plot['SMA20'] = df_for_plot['CLOSE_PRICE'].rolling(20).mean()

# # # Data for plotting
# # data1 = {'x': df_for_plot.DATE,
# #          'open': df_for_plot.OPEN_PRICE,
# #          'close': df_for_plot.CLOSE_PRICE,
# #          'high': df_for_plot.HIGH_PRICE,
# #          'low': df_for_plot.LOW_PRICE,
# #          'type': 'candlestick', }

# # data2 = {'x': df_for_plot.DATE,
# #          'y': df_for_plot.SMA44,
# #          'type': 'scatter',
# #          'mode': 'lines',
# #          'line': {'width': 1, 'color': 'blue'},
# #          'name': 'SMA 44'}

# # data3 = {'x': df_for_plot.DATE,
# #          'y': df_for_plot.SMA20,
# #          'type': 'scatter',
# #          'mode': 'lines',
# #          'line': {'width': 1, 'color': 'red'},
# #          'name': 'SMA 20'}

# # data4 = {'x': df_for_plot.DATE,
# #          'y': df_for_plot.SMA10,
# #          'type': 'scatter',
# #          'mode': 'lines',
# #          'line': {'width': 1, 'color': 'green'},
# #          'name': 'SMA 10 periods'}
# # data = [data1, data2, data3, data4]
# # fig = go.Figure(data=data)

# # # update figure layout
# # fig.update_layout(
# #     title={
# #         'text': "SYMBOL = " + select,
# #         'xanchor': 'left',
# #         'yanchor': 'top'}
# # )

# # st.subheader('Candlestick chart with SMA curves')
# # st.write('Data Range: 04/01/2021 to 30/07/2021')
# # st.plotly_chart(fig)
