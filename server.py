from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from datetime import datetime
import aiohttp  # Import aiohttp for async HTTP requests

app = FastAPI()

async def send_discord_message(unique_id):
    webhook_url = "https://discord.com/api/webhooks/1214662183452016660/1yOSpSVg3oj0gr6rQWnpKW9ncjt-TKeODdlzXE12hWSLwmNlUNOEUI21L3hmxPYCvK5u"
    async with aiohttp.ClientSession() as session:
        webhook = {
            "content": f"ID: {unique_id} APPROVED"
        }
        await session.post(webhook_url, json=webhook)

@app.get('/scan')
async def scan(request: Request):
    # Get the unique ID from the query parameter
    unique_id = request.query_params.get('id')
    
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Record the scan in a text file
    with open('scan_log.txt', 'a') as file:
        file.write(f"ID: {unique_id}, Message: Approved, Timestamp: {timestamp}\n")
    
    # Send the Discord message asynchronously
    await send_discord_message(unique_id)
    
    # Specify the path to your image file
    image_path = './approved.png'
    
    # Return the image file
    return FileResponse(image_path, media_type='image/jpeg')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8181)
    # uvicorn.run(app, host="192.168.0.15", port=5900)
    



# # https://app.cyclic.sh/#/deploy?tab=python
# from fastapi import FastAPI, Request
# from fastapi.responses import FileResponse
# from datetime import datetime

# app = FastAPI()

# @app.get('/scan')
# async def scan(request: Request):
#     # Get the unique ID from the query parameter
#     unique_id = request.query_params.get('id')
    
#     # Get the current timestamp
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     # Record the scan in a text file
#     with open('scan_log.txt', 'a') as file:
#         file.write(f"ID: {unique_id}, Message: Approved, Timestamp: {timestamp}\n")
    
#     # Specify the path to your image file
#     image_path = './approved.png'
    
#     # Return the image file
#     return FileResponse(image_path, media_type='image/jpeg')

# if __name__ == '__main__':
#     import uvicorn
#     # The server listens on 192.168.0.15 at port 5900
#     # uvicorn.run(app, host='192.168.0.15', port=5900)
#     uvicorn.run(app, host="0.0.0.0", port=8181)


# # https://discord.com/api/webhooks/1214662183452016660/1yOSpSVg3oj0gr6rQWnpKW9ncjt-TKeODdlzXE12hWSLwmNlUNOEUI21L3hmxPYCvK5u