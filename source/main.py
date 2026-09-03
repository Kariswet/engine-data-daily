from service.stock_data import StockService
from loguru import logger

import threading
import schedule
import time

def run_thread(func):
    job_thread = threading.Thread(target=func)
    job_thread.start()



if __name__ == "__main__":
    service = StockService()

    schedule.every().day.at("16:00").do(run_thread, service.OHLCVdaily)
    schedule.every().friday.at("16:00").do(run_thread, service.FINANCEreport)
    
    logger.info("Scheduler started. Waiting for next job at 4pm...")

    while True:
        schedule.run_pending()
        time.sleep(1)