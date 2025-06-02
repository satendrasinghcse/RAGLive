from data_downloader import download_raw_data
from data_processor import read_json_file,data_extractor,save_processed_data
from datetime import date
from pathlib import Path
import asyncio



async def data_update():
    today = date.today()
    outer_file = Path(__file__).resolve().parent.parent.parent
    API_URL = f"https://www.federalregister.gov/api/v1/documents.json?per_page=200&conditions[publication_date][is]={today}"
    await download_raw_data(API_URL, f"{outer_file}/data/raw/{today}.json")
    fl = await read_json_file(f"{outer_file}/data/raw/{today}.json")
    ex_data = await data_extractor(fl)
    await save_processed_data(ex_data,f"{today}.json")



if __name__=="__main__":
    asyncio.run(data_update())
    



