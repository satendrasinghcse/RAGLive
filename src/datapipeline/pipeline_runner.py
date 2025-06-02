import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from dailydata_update import data_update

async def my_job():
    datetime.now()
    await data_update()


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(my_job, 'cron', hour=23, minute=00)

    print("Scheduler started with daily jobs at 11 PM.")
    scheduler.start()

    while True:
        await asyncio.sleep(3600) 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
