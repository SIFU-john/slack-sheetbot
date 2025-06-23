from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slack_handlers import handle_event, handle_slash_command

app = FastAPI()

@app.post("/slack/command")
async def slack_command(req: Request):
    return await handle_slash_command(await req.form())

@app.post("/slack/events")
async def slack_event(req: Request):
    body = await req.json()
    
    # ✅ Handle Slack's URL verification request
    if body.get("type") == "url_verification":
        return JSONResponse(content={"challenge": body["challenge"]})
    
    # ✅ Forward other events to handler
    return await handle_event(body)
