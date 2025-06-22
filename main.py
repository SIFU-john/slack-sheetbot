from fastapi import FastAPI, Request
from slack_handlers import handle_slash_command, handle_event

app = FastAPI()

@app.post("/slack/command")
async def slack_command(req: Request):
    return await handle_slash_command(await req.form())

@app.post("/slack/events")
async def slack_event(req: Request):
    body = await req.json()
    return await handle_event(body)
