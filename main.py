import schedule
import time

import monitor

if __name__ == "__main__":

    print("Starting watching")

    schedule.every(20).seconds.do(monitor.monitor)
    while True:
        schedule.run_pending()
        time.sleep(1)