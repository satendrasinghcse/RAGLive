from datapipeline.database import get_pool, fetch_data
import asyncio
from dotenv import load_dotenv
import os
import re
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("groq_api_key")
client = Groq()


async def llm_generate_sql(question: str) -> str:
    prompt = f"""Convert this user question into a MySQL query:
        Question: "{question}"
        SQL:"""
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that converts user questions into single MySQL query and you have orders table which have these columns title, abstract, type, agency_name, publication_date",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            result += content

    return result.strip()


async def llm_summarize_result(user_query: str, data: list) -> str:
    prompt = f"""
    The user asked: "{user_query}"
    Here is the raw data: {data}
    Provide a helpful, user-friendly summary of this data.
    """
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You summarize database results into plain English for users.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    result = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            result += content

    return result.strip()



async def llm_runner(question):
    qry = await llm_generate_sql(question)
    sql_queries = re.findall(r"```sql\n(.*?)```", qry, re.DOTALL)
    real_query = ""
    for i, query in enumerate(sql_queries, 1):
        real_query = query.strip()
        break
    pool = await get_pool()
    dt = await fetch_data(pool, real_query)
    pool.close()
    await pool.wait_closed()
    rs = await llm_summarize_result(question, dt)
    return rs


if __name__ == "__main__":
    #asyncio.run(main())
    pass
