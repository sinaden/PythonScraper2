from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import date
import datetime

import pandas as pd

row = 0
today = date.today()


a = [[], [],   [],     [],    [],        [],    [],    [],    [],   [],  [],   []] 
# Brand, Model, Memory, Color, Condition, Price, Title, Desc, link, id, posted, scraped
# 0      1       2       3       4        5         6    7      8   9   10       11 

def dba_scraper_start(url):
    global row
    print(url)
    # opening up connection, grabbing the page
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    
    

    page_soup = soup(page_html, "html.parser")


#    list_item = page_soup.findAll("a",{"class":"link-to-listing"})
        
    
    list_item = page_soup.findAll("tr",{"class":"dbaListing"})
    for item in list_item:
        
        pd = item.findAll("td", {"title":"Dato"})
        posted_date = pd[0].text
        link = item.findAll("a", {"class":"thumbnailContainerInner"})
        url = link[0]['href']
        scrape_one(url, row, posted_date)
        row += 1
    






def scrape_one(url, row, date_posted):
    pnt = 0
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    a[0].append('Uden')
    a[1].append('Uden')
    a[2].append('Uden')
    a[3].append('Uden')
    a[4].append('Uden')
    a[5].append('Uden')
    a[6].append('Uden')
    a[7].append('Uden')
    a[8].append('Uden')
    a[9].append('Uden')
    a[10].append('Uden')
    a[11].append(today.strftime("%d/%m/%Y"))
    

    page_soup = soup(page_html, "html.parser")
    
    price = page_soup.findAll("span", {"class":"price-tag"})
    
    #print("price ", price[0].text)
    
    #date_posted = page_soup.findAll("span", {"class": "heading-small muted"})
    #date_posted_clear = date_posted[0].text.strip()
    
    
    if "I går" in date_posted:
        yesterday = today - datetime.timedelta(days = 1)
        a[10][row] = yesterday.strftime("%d/%m/%Y")
    elif "I dag" in date_posted:
        a[10][row] = today.strftime("%d/%m/%Y")
    else :
        date_posted += " " + str(today.year)
        dformat={'maj':'may', 'okt':'oct'}
        dt = date_posted.strip()
        for w, i in dformat.items():
            dt = dt.replace(w, i)
    
        dt= pd.to_datetime(dt, format='%d. %b %Y')
        a[10][row] = dt.strftime("%d/%m/%Y")
        
    
    str_1 = price[0].text
    
    
    str_st = str_1.find("kr.")

    s = str_1[:str_st].strip()
    s = s.replace(".", "")

    a[5][row] = s
    
    a[8][row] = url
    
    strId = url.find("id-")
    a[9][row] = url[strId + 3:][:-1]
    
    desc = page_soup.findAll("meta", {"property":"og:description"})
    a[7][row] = desc[0]['content']
    
    ti = page_soup.findAll("div", {"class":"vip-heading"})
    st0 = ti[0].text.strip()
    k1 = st0.find("\n")
    
    a[6][row] = st0[:k1]

    
    
    item = page_soup.findAll("div",{"class":"vip-matrix-data"})
    k = item[0].findAll("td")
    cnt = 0
    for cat in k:
        cat = cat.text
        if len(cat) == 0:
            continue
        
        if cat == "Mærke":
            #a[0][row] 
            pnt = 0
        if cat == "Hukommelse":
            #a[2][row] 
            pnt = 2
        if cat == "Model":
            #a[1][row] 
            pnt = 1
        if cat == "Stand":
            #a[4][row] 
            pnt = 4
        if cat == "Farve":
            #a[3][row] 
            pnt = 3
        
        if cnt % 2 == 1:
            if pnt == 2:
                mem = cat
                str2 = 'GB gb m'
                mem2 = ''.join(c for c in mem if c not in str2)
                a[pnt][row] = mem2
            else:
                a[pnt][row] = cat
    
        cnt += 1

        
        
        
        
def write_to_sheet():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    import pprint


    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Python Autoscrapers')

    my_list = [[' ' for x in range(12)] for y in range(3600)] 

    data_size = len(a[1])
    #my_list[0] = ["Brand","Model","Memory", "Color", "Condition", "Price", "Title", "Des", "URL", "id", "d post", "d scrape"]
    for i in range(0, data_size):
        for j in range(0, 12):
            my_list[i][j] = a[j][i]

    sheet.values_append(
        range='Smartphones-CPH!A1', 
        params={'valueInputOption': 'RAW'}, 
        body={'values': my_list}
    )

    
    
    
def importTo_clean_sheet():
    from gspread_pandas import Spread, Client
    import gspread_pandas as gp
    import datetime
    import numpy as np
    import pandas as pd
    import re
    import importlib
    #import cleaner 
    #cleaner = importlib.reload(cleaner)
    #from cleaner import cleaning_and_to_sql

    pd.set_option('display.max_rows', 20)
    pd.set_option('display.max_columns', 50)

    s = Spread('work','Python Autoscrapers')
    
    df1 = s.sheet_to_df(index = 0, start_row = 1, header_rows=1, sheet = "Smartphones-CPH").astype(str)
    import time 
    from datetime import datetime
    from datetime import timedelta
    for i in ['Model', 'Brand', 'Color', 'Condition']:
        df1[i] = df1[i].str.lower()
        
    dups_ids = df1.pivot_table(index=['id'], aggfunc='size')
    type(dups_ids)
    di = dups_ids.to_frame()
    di.head()

    di.columns = ['days active']
    di.reset_index(inplace = True)

    df1 = pd.merge(df1, di, on='id')
    df1 = df1.drop_duplicates(subset='id', keep='first')

    filter = df1["d scrape"] != " "
    df1 = df1[filter]
    
    df1['state'] = "Not sold yet"
    
    #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    for stdat, ndays, idx in zip(df1['d scrape'], df1['days active'], df1.index):
        do = datetime.strptime(stdat, '%d/%m/%Y')
        ndays -= 1
        do = do + timedelta(days = ndays)
        tod = datetime.strptime(today.strftime("%d/%m/%Y"), '%d/%m/%Y')




        if do < tod:
            df1.state[idx] = 'Sold'
       # print(do.strftime("%d/%m/%Y"), "   ", stdat, " today", today.strftime("%d/%m/%Y"))
    
    s = Spread('work','Python Autoscrapers')
    s.df_to_sheet(df1, index=False, sheet='Smartphones-CPH/Clean', start='A2', replace=True)
    
    
    
    
def startSmartPhoneCPH():
    print("Helloo, We are going to scrape smartphones in DBA")

    for i in range(1, 2):
        url = 'https://www.dba.dk/mobil-og-telefoni/mobiltelefoner-og-tilbehoer/mobiltelefoner/side-' + str(i)
        dba_scraper_start(url)
    
    print("Scrape is done now we are going to write the data to the sheet")

    write_to_sheet()

    print("Data has been inputted to first Sheet now its time to clean it")
    
    importTo_clean_sheet()
    
    print("Data has been cleaned and imported to second sheet- Case closed")
    
    

    
    
    
#startSmartPhoneCPH()
