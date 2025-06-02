import aiohttp
import asyncio
import aiofiles
import json
from datetime import date, timedelta
from pathlib import Path


async def download_raw_data(
    url: str, filename: str = "data/federal_register_data.json"
):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()

            async with aiofiles.open(filename, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, indent=2))

            print(f"Data saved to {filename}")
            return data
            


async def get_date_range(start_date: date, end_date: date) -> list:
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return date_list


async def main():
    start = date(2025, 1, 1)
    end = date(2025, 5, 31)
    dt = await get_date_range(start, end)
    outer_file = Path(__file__).resolve().parent.parent.parent
    for i in dt:
        API_URL = f"https://www.federalregister.gov/api/v1/documents.json?per_page=200&conditions[publication_date][is]={i}"
        await download_raw_data(API_URL, f"{outer_file}/data/raw/{i}.json")


if __name__ == "__main__":
    asyncio.run(main())
