from src.non_spiders import ComodityIndex, Credit, ExchangeRate, LsCafef, LsLnh, LsNhtm
import threading
import sys

if __name__=='__main__':
    commodity_index = ComodityIndex.ComodityIndex()
    credit = Credit.Credit()
    exchange_rate = ExchangeRate.ExchangeRate()
    ls_cafef = LsCafef.LsCafef()
    ls_lnh = LsLnh.LsLnh()
    ls_nhtm = LsNhtm.LsNhtm()
    
    # Create threads
    commodity_index_thread = threading.Thread(target=commodity_index.run)
    credit_thread = threading.Thread(target=credit.run)
    exchange_rate_thread = threading.Thread(target=exchange_rate.run)
    ls_cafef_thread = threading.Thread(target=ls_cafef.run)
    ls_lnh_thread = threading.Thread(target=ls_lnh.run)
    
    # Start threads
    commodity_index_thread.start()
    credit_thread.start()
    exchange_rate_thread.start()
    ls_cafef_thread.start()
    ls_lnh_thread.start()
    
    # Wait for threads to finish their jobs
    commodity_index_thread.join()
    credit_thread.join()
    exchange_rate_thread.join()
    ls_cafef_thread.join()
    ls_lnh_thread.join()
    
    # ls_nhtm.run() # This one cannot be run in a thread since it use tabula to parse pdf (jvm cannot be run in a thread)
    
    print('All threads finished their jobs')
    sys.exit(0)

    