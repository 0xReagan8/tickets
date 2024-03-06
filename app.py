from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse
import aiohttp
from pydantic import BaseModel
import requests
import json

app = FastAPI()

WEBHOOK_URL = "https://discord.com/api/webhooks/1214662183452016660/1yOSpSVg3oj0gr6rQWnpKW9ncjt-TKeODdlzXE12hWSLwmNlUNOEUI21L3hmxPYCvK5u"

class Item(BaseModel):
    item_id: int

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')

@app.get("/item/{item_id}")
async def read_item(item_id: int):

    embed = {
        "title": "🚀",
        "description": "Event ID: <EVENT ID>\nTicket ID: <TICKET ID>\nScan Time: <SCAN TIME>\n\nhttps://sore-cyan-ostrich-fez.cyclic.app",
        "color": 1543684, 
        "fields": [],
        "footer": {
            "text": "** use report URL to get a text listing of all activity"
        }
    }

    # Wrap the embed in a payload as Discord expects
    payload = {
        "embeds": [embed],
    }

    # Convert the payload to JSON and make the POST request to the webhook URL
    response = requests.post(WEBHOOK_URL, json=payload)

    return {"item_id": item_id}


@app.get("/items/")
async def list_items():
    return [{"item_id": 1, "name": "Foo"}, {"item_id": 2, "name": "Bar"}]

@app.post("/items/")
async def create_item(item: Item):
    return item



Get an item: curl -i -XGET http://localhost:8181/item/1
List items: curl -i -XGET http://localhost:8181/items/
Post an item: curl -i -XPOST http://localhost:8181/items/ --data '{"item_id":1,"name":"Bob"}' -H 'content-type: application/json'

curl -i -XGET https://sore-cyan-ostrich-fez.cyclic.app/
curl -i -XGET https://sore-cyan-ostrich-fez.cyclic.app/item/1
curl -i -XGET https://sore-cyan-ostrich-fez.cyclic.app/items/
curl -i -XPOST https://sore-cyan-ostrich-fez.cyclic.app/items/ --data '{"item_id":1,"name":"Bob"}' -H 'content-type: application/json'



# import aiohttp
# from fastapi import FastAPI, Request
# from fastapi.responses import FileResponse, PlainTextResponse
# from datetime import datetime
# from pydantic import BaseModel

# app = FastAPI()

# WEBHOOK_URL = "https://discord.com/api/webhooks/1214662183452016660/1yOSpSVg3oj0gr6rQWnpKW9ncjt-TKeODdlzXE12hWSLwmNlUNOEUI21L3hmxPYCvK5u"



# def build_embed(ticket_id, event_id, timestamp, base_url):
#     embed = {
#         "title": "🚀",
#         "description": f"Event ID: {event_id}\nTicket ID: {ticket_id}\nScan Time: {timestamp}\n\n{str(base_url)}/list",
#         "color": 1543684,
#         "fields": [],
#         "footer": {
#             "text": "** use report URL to get a text listing of all activity"
#         }
#     }
#     return embed

# async def send_discord_message(embed):
#     async with aiohttp.ClientSession() as session:
#         payload = {"embeds": [embed]}
#         async with session.post(WEBHOOK_URL, json=payload) as response:
#             if response.status == 204:
#                 print("Embed sent successfully!")
#             else:
#                 response_text = await response.text()
#                 print(f"Failed to send embed. Status code: {response.status} - Response: {response_text}")

# # @app.get("/item/{item_id}")
# # async def read_item(item_id: int):
# #     return {"item_id": item_id}


# @app.get('/scan{event_id, ticket_id}')
# async def scan(request: Request):
#     base_url = request.base_url
#     event_id = request.query_params.get('event_id')
#     ticket_id = request.query_params.get('ticket_id')
#     timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')

#     # try:
#     #     with open('scan_log.txt', 'a') as file:
#     #         file.write(f"EVENT_ID:{event_id}, TICKET_ID: {ticket_id}, STATUS: Approved, Timestamp: {timestamp}\n")
#     # except IOError as e:
#     #     print(f"Error writing to log file: {e}")

#     embed = build_embed(ticket_id, event_id, timestamp, base_url)
#     await send_discord_message(embed)

#     image_path = './approved.png'
#     return FileResponse(image_path, media_type='image/jpeg')

# # @app.get('/list')
# # async def list_logs(request: Request):
# #     try:
# #         with open('scan_log.txt', 'r') as file:
# #             file_contents = file.read()
# #         return PlainTextResponse(file_contents)
# #     except IOError as e:
# #         return PlainTextResponse(f"Error reading log file: {e}", status_code=500)
