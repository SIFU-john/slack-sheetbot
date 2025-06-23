import os
from slack_sdk.web.async_client import AsyncWebClient
from mistral_agent import answer_query
from spreadsheet_parser import parse_file

from dotenv import load_dotenv
load_dotenv()

client = AsyncWebClient(token=os.getenv("SLACK_BOT_TOKEN"))

async def handle_slash_command(payload):
    user_id = payload["user_id"]
    channel_id = payload["channel_id"]
    await client.chat_postMessage(channel=channel_id, text=f"Hi <@{user_id}>! Upload your spreadsheet and ask a question.")

async def handle_event(event):
    if "event" in event and event["event"]["type"] == "message":
        file_info = event["event"].get("files", [{}])[0]
        if file_info.get("mimetype", "").startswith("application/vnd"):
            url = file_info["url_private_download"]
            headers = {"Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"}
            df = await parse_file(url, headers)
            query = event["event"].get("text", "")
            answer = await answer_query(df, query)
            await client.chat_postMessage(channel=event["event"]["channel"], text=answer)
        else:
            await client.chat_postMessage(channel=event["event"]["channel"], text="Please upload a valid Excel or CSV file.")
    return {"ok": True}
