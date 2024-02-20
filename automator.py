import schedule, time
from main import scrape_stockx_data

def job():
    scrape_stockx_data()
    print("Scraping data")

schedule.every(24).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)