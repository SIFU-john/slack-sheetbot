import pandas as pd
import io
import aiohttp

async def parse_file(file_url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url, headers=headers) as resp:
            content = await resp.read()
            try:
                return pd.read_excel(io.BytesIO(content))
            except:
                return pd.read_csv(io.BytesIO(content))
