from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.dba.dk/computer-og-spillekonsoller/mac/?pris=(1000-)' 

#opening up connection, grabbing / downloading the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html, "html.parser")

#grabs each product
containers = page_soup.findAll("tr", {"class": "dbaListing"})

for container in containers:
    description = container.findAll("a", {"class": "listingLink"})
    description_clear = description[1].text.strip()
    
    date = container.findAll("td", {"title": "Dato"});
    date_clear = date[0].text.strip()

    price = container.findAll("td", {"title": "Pris"});
    price_clear = price[0].text.strip()

    print("\n--------------------------")
    #print("\n<<<DESCRIPTION<<<<<<<")
    #print(description_clear)
    #print(">>>>>>>>>>>>>>>>>>>>>\n")
    print("Date is: " + date_clear)
    print("Price is: " + price_clear)
    print("--------------------------\n")