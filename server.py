from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI()

@app.get('/scan')
async def scan(request: Request):
    # Get the unique ID from the query parameter
    unique_id = request.query_params.get('id')
    
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Record the scan in a text file
    with open('scan_log.txt', 'a') as file:
        file.write(f"ID: {unique_id}, Message: Approved, Timestamp: {timestamp}\n")
    
    # Specify the path to your image file
    image_path = './approved.png'
    
    # Return the image file
    return FileResponse(image_path, media_type='image/jpeg')

if __name__ == '__main__':
    import uvicorn
    # The server listens on 192.168.0.15 at port 5900
    uvicorn.run(app, host='192.168.0.15', port=5900)




# from flask import Flask, request, send_file
# from datetime import datetime

# app = Flask(__name__)

# @app.route('/scan')
# def scan():
#     # Get the unique ID from the query parameter
#     unique_id = request.args.get('id')
    
#     # Get the current timestamp
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     # Record the scan in a text file
#     with open('scan_log.txt', 'a') as file:
#         file.write(f"ID: {unique_id}, Message: Approved, Timestamp: {timestamp}\n")
    
#     # Specify the path to your image file
#     image_path = './approved.png'
    
#     # Return the image file
#     return send_file('./approved.png', mimetype='image/jpeg')

# if __name__ == '__main__':
#     # The server listens on 192.168.0.15 at port 5900
#     app.run(host='192.168.0.15', port=5900, debug=True)
