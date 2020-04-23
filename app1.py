import main_package.dba_package.macbooks_package.MacBookCPH as DBA_mac_cph
import main_package.dba_package.smartphones_package.SmartPhoneCPH as DBA_phone_cph



import time
import schedule


def main():
    print("\n")
    print("/////////////////////////////////////////////////////")
    print("///////////////Welcome to the APP1///////////////////")
    print("//////////////////////////////////////////////////////")
    print("//////////////////////////////////////////////////////")

    print("\n \n       MacBook Scraper ready to launch : \n \n \n")
    DBA_mac_cph.startMacBookCPH()

    print("\n \n       Smartphone Scraper ready to launch : \n \n \n \n")
    DBA_phone_cph.startSmartPhoneCPH()

    print("\n - - - - - - - See you in the next round - - - - \n ")


#schedule.every().hour.do(main)
#schedule.every(10).minutes.do(main)
#schedule.every().day.at('13:20').do(main)
schedule.every(120).seconds.do(main)

while 1:
    schedule.run_pending()
    time.sleep(1)
#main()
schedule.clear()
