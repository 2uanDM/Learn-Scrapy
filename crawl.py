from src.non_spiders import ComodityIndex, Credit, ExchangeRate, LsCafef, LsLnh, LsNhtm, Gdp
import threading
import sys

if __name__ == '__main__':
    commodity_index = ComodityIndex.ComodityIndex()
    credit = Credit.Credit()
    exchange_rate = ExchangeRate.ExchangeRate()
    ls_cafef = LsCafef.LsCafef()
    ls_lnh = LsLnh.LsLnh()
    ls_nhtm = LsNhtm.LsNhtm()
    gdp = Gdp.Gdp()

    # Create threads
    credit_thread = threading.Thread(target=credit.run)
    exchange_rate_thread = threading.Thread(target=exchange_rate.run)
    ls_cafef_thread = threading.Thread(target=ls_cafef.run)
    ls_lnh_thread = threading.Thread(target=ls_lnh.run)

    # Start threads
    credit_thread.start()
    exchange_rate_thread.start()
    ls_cafef_thread.start()
    ls_lnh_thread.start()

    # Wait for threads to finish their jobs
    credit_thread.join()
    exchange_rate_thread.join()
    ls_cafef_thread.join()
    ls_lnh_thread.join()

    # Proxy for crawling shfe pages if needed

    auth_proxy = {
        'host': '185.191.228.63',
        'port': 30032,
        'username': 'ebay2023',
        'password': 'proxyebaylam'
    }

    # gdp.run()
    ls_nhtm.run()  # This one cannot be run in a thread since it use tabula to parse pdf (jvm cannot be run in a thread)
    commodity_index.run(auth_proxy)

    print('All threads finished their jobs')
    sys.exit(0)
