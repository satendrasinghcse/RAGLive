import aiofiles
import json
import asyncio
import os
from pathlib import Path


async def read_json_file(filename: str):
    async with aiofiles.open(filename, mode="r", encoding="utf-8") as file:
        contents = await file.read()
        data = json.loads(contents)
        return data


async def data_extractor(data):
    # filename = "federal_register_data.json"
    # data = await read_json_file(filename)
    title = data["results"][0]["title"]
    abstract = data["results"][0]["abstract"]
    type = data["results"][0]["type"]
    agencies_name = data["results"][0]["agencies"][0]["name"]
    publication_date = data["results"][0]["publication_date"]

    return {
        "title": title,
        "abstract": abstract,
        "type": type,
        "agencies_name": agencies_name,
        "publication_date": publication_date,
    }


async def save_processed_data(dict, dt):
    # json_data = json.dumps(dict)
    new_path = Path(__file__).resolve().parent.parent.parent/"data/processed"
    async with aiofiles.open(f"{new_path}/{dt}", "w", encoding="utf-8") as f:
        await f.write(json.dumps(dict, indent=2))
        print(f"Data saved to {new_path}/{dt}")


folder_path = Path(__file__).resolve().parent.parent.parent/"data/raw"
json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]


async def main():
    # rd = await read_json_file("data/raw/2025-01-02.json")
    # tr = await data_extractor(rd)
    # print(tr)
    for file_name in json_files:
        # print(f"{folder_path}/{file_name}")
        files_path = f"{folder_path}/{file_name}"
        rd = await read_json_file(files_path)
        if rd["count"] != 0:
            dt = await data_extractor(rd)
            await save_processed_data(dt, file_name)


if __name__ == "__main__":
    asyncio.run(main())
