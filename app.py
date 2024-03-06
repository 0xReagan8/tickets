from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from datetime import datetime
import aiohttp

app = FastAPI()
#fk;dlk;f
async def send_discord_message(message):
    webhook_url = "https://discord.com/api/webhooks/1214662183452016660/1yOSpSVg3oj0gr6rQWnpKW9ncjt-TKeODdlzXE12hWSLwmNlUNOEUI21L3hmxPYCvK5u"
    async with aiohttp.ClientSession() as session:
        webhook = message
        await session.post(webhook_url, json=webhook)

def format_embed(ticket_id, event_id, timestamp, base_url ):
    embeded_message = """{
    "content": "😊 Ticket Scanned for Event:  🎉  EVENT NAME ✨",
    "tts": false,
    "embeds": [
        {
        "id": 652627557,
        "title": "🚀",
        "description": "Event ID: {event_id}\nTicket ID: {ticket_id}\nScan Time: {timestamp}\n\n{base_url}/list}",
        "color": 1543684,
        "fields": [],
        "footer": {
            "text": "** use report URL to get a text listing of all activity"
        }
        }
    ],
    "components": [],
    "actions": {}
    }"""

    return(embeded_message)

@app.get('/scan')
async def scan(request: Request):
    # Get the unique ID from the query parameter
    base_url = request.base_url
    event_id = request.query_params.get('event_id')
    ticket_id = request.query_params.get('ticket_id')
  
    # Get the current timestamp
    timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
      
    # Record the scan in a text file
    with open(f'scan_log.txt', 'a') as file:
        file.write(f" EVENT_ID:{event_id},  TICKET_ID: {ticket_id}, STATUS: Approved, Timestamp: {timestamp}\n")
    
    # create the embedded message
    message = format_embed(ticket_id, event_id, timestamp, base_url )

    # Send the Discord message asynchronously
    await send_discord_message(message)
    
    # Specify the path to your image file
    image_path = './approved.png'
    
    # Return the image file
    return FileResponse(image_path, media_type='image/jpeg')

@app.get('/list')
async def list(request: Request):
    # Record the scan in a text file
    with open('scan_log.txt', 'r') as file:
        file_contents = file.read()

    return(FileResponse(file_contents))
