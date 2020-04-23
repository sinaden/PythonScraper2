from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from datetime import date
import pandas as pd

import re

row = 0
today = date.today()
a = [ [],      [],         [],           [],          [],           [],      [],         [],          [],        [],       [],        [],          [],      [],         [],                []  ] 
#     Brand    Type     Display Size    Year     Product Model  Processor   RAM       Hard Drive     Stand      Price     Title     Description   Link     DBA ID      Date posted    Date scraped
#      0        1           2            3            4             5        6            7           8          9         10         11           12       13           14                15

def dba_scraper_start(url):
    global row
    print(url)
    # opening up connection, grabbing / downloading the page
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    #html parsing
    page_soup = soup(page_html, "html.parser")

    #grabs each Macbook
    #list_item = page_soup.findAll("a",{"class":"link-to-listing"})

    list_item = page_soup.findAll("tr",{"class":"dbaListing"})
    for item in list_item:
        
        pd = item.findAll("td", {"title":"Dato"})
        posted_date = pd[0].text.strip()
        link = item.findAll("a", {"class":"thumbnailContainerInner"})
        url = link[0]['href']
        #print ('URL IS --- ', url)
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
    a[11].append('Uden')
    a[12].append('Uden')
    a[13].append('Uden')
    a[14].append('Uden')
    a[15].append(today.strftime("%d/%m/%Y"))
    
    #html parsing the downloaded page
    page_soup = soup(page_html, "html.parser")
    
    #scrape the title
    title = page_soup.findAll("h1")
    title_clear = title[0].text.strip()
    #print (title_clear)
    a[10][row] = title_clear
    #print (title_clear, "\n")
    
    strId = url.find("/id-")
    #print (url[strId + 4:][:-1])
    a[13][row]=url[strId + 4:][:-1]
    
    #date_posted = page_soup.findAll("span", {"class": "heading-small muted"})
    #date_posted_clear = date_posted[0].text.strip()
    #a[14][row] = date_posted_clear
    if "I går" in date_posted:
        yesterday = today - datetime.timedelta(days = 1)
        a[14][row] = yesterday.strftime("%d/%m/%Y")
    elif "I dag" in date_posted:
        a[14][row] = today.strftime("%d/%m/%Y")
    else :
        date_posted += " " + str(today.year)
        dformat={'maj':'may', 'okt':'oct'}
        dt = date_posted
        
        for w, i in dformat.items():
            dt = dt.replace(w, i)
    
        dt= pd.to_datetime(dt, format='%d. %b %Y')
        a[14][row] = dt.strftime("%d/%m/%Y")
    
    price = page_soup.findAll("span", {"class": "price-tag"})
    price_clear = price[0].text.strip()
    price_clear = price_clear.replace("kr.", "")
    price_clear = price_clear.replace(".", "")
    #print("Price is: " + price_clear)
    
    a[9][row] = price_clear
    a[12][row] = url
    
    description = page_soup.findAll("div", {"class": "vip-additional-text"})
    description_clear = description[0].text.strip()
    #print(description_clear)
    
    a[11][row] = description_clear
    
    matrix = page_soup.findAll("div", {"class": "vip-matrix-data"})
    cells = matrix[0].findAll("td")
    cnt = 0
    my_substring = "Mac"
    for cell in cells:
        cell = cell.text
        if len(cell) == 0:
            continue
            
        if cell == "Type":
            pnt = 1
            
        if cell == "Ram (GB)":
            pnt = 6
            
        if cell == "Produkt/model":
            pnt = 4
            
        if cell == "Harddisk (GB)":
            pnt = 7
            
        if cell == "Processor (GHz)":
            pnt = 5
            
        if cell == "Stand":
            pnt = 8
    
        if pnt == 1 and my_substring.lower() in cell.lower():
            a[0][row] = "Apple"
        
        if cnt % 2 == 1:
            a[pnt][row] = cell
        cnt +=1
    
    #display_size
    #print (a[4][row].split())
    display_size = ''
    product_model_array = a[4][row].split()
    for element in product_model_array:
        if element.find('\"') > 0:
            display_size = element
        if element.find('”') > 0:
            display_size = element
        if element.find('-inch') > 0:
            display_size = element
        #if element.find('inch'):
            #display_size = product_model_array[product_model_array.index(element)-1]
    #print (display_size, '\n')
    if display_size != '':
        display_size = display_size.replace("-inch", "\"")
        display_size = display_size.replace("-inch,", "\"")
        display_size = display_size.replace("-inch)", "\"")
        display_size = display_size.replace("(", "")
        display_size = display_size.replace(", ", "")
        display_size = display_size.replace(",", ".")
        display_size = display_size.replace("”", "\"")
        
        #print (display_size, ' - ', display_size.split("\"")[0] + "\"", '\n')
        a[2][row] = display_size.split("\"")[0] + "\""
    
    #year
    year_season = ''
    year_number = ''
    year = ''
    for element in product_model_array:
        match = re.search(r'\d*([2][0-1][0-9]{2})', element)
        if match is not None:
            #print (match.group(), "\n")
            year_number = match.group()
            
    if "Late" in product_model_array:
        year_season = "late "

    if "late" in product_model_array:
        year_season = "late "

    if "mid" in product_model_array:
        year_season = "mid "

    if "Mid" in product_model_array:
        year_season = "mid "

    if "midt" in product_model_array:
        year_season = "midt "

    if "Midt" in product_model_array:
        year_season = "midt "

    if "Early" in product_model_array:
        year_season = "early "

    if "early" in product_model_array:
        year_season = "early "

    if "Medio" in product_model_array:
        year_season = "medio "

    if "medio" in product_model_array:
        year_season = "medio "

    if "Ultimo" in product_model_array:
        year_season = "ultimo "

    if "ultimo" in product_model_array:
        year_season = "ultimo "

    if "Primo" in product_model_array:
        year_season = "primo "

    if "primo" in product_model_array:
        year_season = "primo "
    
    year = year_season + year_number
    #print (year, '\n')
    if year != '':
        a[3][row] = year.strip()
        
        
        
  


    

    
def write_to_sheet():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    import pprint


    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Python Autoscrapers')

    my_list = [[' ' for x in range(16)] for y in range(len(a[0]) + 3)] 

    #my_list[0] = ["Brand", "Type", "Display Size", "Year", "Product Model", "Processor", "RAM", "Hard Drive", "Stand", "Price", "Title", "Description", "Link", "DBA ID", "Date Posted", "Date Scraped"]

    for i in range(0, len(a[0])):
        for j in range(0, 16):
            #print(a[j][i] + " ")
            my_list[i][j] = a[j][i]

    #print(my_list)    

    sheet.values_append(
        range='Macbooks-CPH!A1', 
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
    df1 = s.sheet_to_df(index = 0, start_row = 1, header_rows=1, sheet = "Macbooks-CPH").astype(str)

    import time 
    from datetime import datetime
    
    from datetime import timedelta

    dups_ids = df1.pivot_table(index=['DBA ID'], aggfunc='size')
    type(dups_ids)
    di = dups_ids.to_frame()
    di.head()

    di.columns = ['days active']
    di.reset_index(inplace = True)
    
    df1 = pd.merge(df1, di, on='DBA ID')
    df1 = df1.drop_duplicates(subset='DBA ID', keep='first')

    filter = df1["Date Scraped"] != " "
    df1 = df1[filter]
    
    df1['state'] = "Not sold yet"
    
    
    #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    for stdat, ndays, idx in zip(df1['Date Scraped'], df1['days active'], df1.index):
        do = datetime.strptime(stdat, '%d/%m/%Y')
        ndays -= 1
        do = do + timedelta(days = ndays)
        tod = datetime.strptime(today.strftime("%d/%m/%Y"), '%d/%m/%Y')




        if do < tod:
            df1.state[idx] = 'Sold'
       # print(do.strftime("%d/%m/%Y"), "   ", stdat, " today", today.strftime("%d/%m/%Y"))
    
    s = Spread('work','Python Autoscrapers')
    s.df_to_sheet(df1, index=False, sheet='Macbooks-CPH/Clean', start='A2', replace=True)
        

        
        
        
        
        
def startMacBookCPH():
    #for i in range(1, 57):

    print ("Hello, Mcbook scraper is going to start soon")
    for i in range(1, 2):
        url = 'https://www.dba.dk/computer-og-spillekonsoller/mac/side-' + str(i) + '/?pris=(1000-)'
        dba_scraper_start(url)
        
        
    print("Scrape is done now we are going to write the data to the sheet")

    write_to_sheet()

    print("Data has been inputted to first Sheet now its time to clean it")
    
    importTo_clean_sheet()
    
    print("Data has been cleaned and imported to second sheet- Case closed")
    
    
    
#startMacBookCPH()
    