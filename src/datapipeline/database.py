import asyncio
import aiomysql
from datapipeline.data_processor import read_json_file
from pathlib import Path
import os


async def fetch_data(pool, query):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query)
            results = await cur.fetchall()
            return results


async def get_pool():
    return await aiomysql.create_pool(
        host="localhost", user="root", password="admin", db="my_db"
    )


async def create_table(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                              id INT AUTO_INCREMENT PRIMARY KEY,
                              title TEXT,
                              abstract TEXT,
                              type VARCHAR(100),
                              agency_name VARCHAR(255),
                              publication_date DATE );

            """
            )
            print("Table created or already exists.")


async def insert_data(pool, title, abstract, type, agency_name, publication_date):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                              INSERT INTO orders (title, abstract, type, agency_name, publication_date)
                              VALUES (%s, %s, %s, %s, %s)""",
                (title, abstract, type, agency_name, publication_date),
            )
            await conn.commit()
            print(f"Data Inserted Successfully!")


async def main():
    pool = await get_pool()

    await create_table(pool)
    folder_path = Path(__file__).resolve().parent.parent.parent/"data/processed"
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    for file_name in json_files:
        dt = await read_json_file(f"{folder_path}/{file_name}")
        await insert_data(
            pool,
            dt["title"],
            dt["abstract"],
            dt["type"],
            dt["agencies_name"],
            dt["publication_date"],
        )

    pool.close()
    await pool.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
