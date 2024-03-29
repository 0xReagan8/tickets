import os
from datetime import datetime, timedelta
import requests
import logging
from flask import Flask, Response, request, render_template, render_template_string

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def format_timestamp(timestamp):
    from datetime import datetime

    # Convert milliseconds to seconds
    timestamp_in_seconds = timestamp / 1000

    # Convert to a datetime object
    dt_object = datetime.fromtimestamp(timestamp_in_seconds)

    # Format the datetime object to a string in AM/PM format
    formatted_time = dt_object.strftime('%Y-%m-%d %I:%M:%S %p')

    return(formatted_time)

def write_pickle(data:dict, event_id:str):
    import pickle
    from b2sdk.v1 import InMemoryAccountInfo, B2Api

    pickled_data = pickle.dumps(data)

    # Initialize the B2 API with your account information
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    application_key_id = os.getenv("KEY_ID")
    application_key = os.getenv("APPLICATION_KEY")
    b2_api.authorize_account("production", application_key_id, application_key)

    # Specify your bucket
    bucket = b2_api.get_bucket_by_name(os.getenv("BUCKET_NAME"))

    file_name = f"{event_id}.pck"  # The name of the file in B2

    # Upload the data
    b2_file_version = bucket.upload_bytes(
        data_bytes=pickled_data,
        file_name=file_name
    )
    
def read_pickle(event_id):
    import pickle
    from b2sdk.v1 import InMemoryAccountInfo, B2Api, DownloadDestBytes

    # Initialize the B2 API with your account information
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    application_key_id = os.getenv("KEY_ID")
    application_key = os.getenv("APPLICATION_KEY")
    b2_api.authorize_account("production", application_key_id, application_key)

    # Specify your bucket
    bucket = b2_api.get_bucket_by_name(os.getenv("BUCKET_NAME"))
    try:
        # File to download
        file_name = f"{event_id}.pck"  # The name of the file in B2

        # Prepare a DownloadDestBytesIO object for the downloaded file
        download_dest = DownloadDestBytes()

        # Download the file into the DownloadDestBytesIO object
        bucket.download_file_by_name(file_name, download_dest)

        # Access the BytesIO object from download_dest
        bytes_io = download_dest.get_bytes_written()

        # decode the pickle
        d = pickle.loads(bytes_io)

        return(d)
    except:
        return(None)

def list_bucket():
    from b2sdk.v1 import InMemoryAccountInfo, B2Api
    import os

    # Replace these with your actual application key ID and application key
    application_key_id = os.getenv("KEY_ID")
    application_key = os.getenv("APPLICATION_KEY")

    # Set up the B2 API
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", application_key_id, application_key)

    # Get the bucket name from environment variable
    bucket_name = b2_api.get_bucket_by_name(os.getenv("BUCKET_NAME"))

    # List all files in the bucket and print them
    for file_info, folder_name in bucket_name.ls(show_versions=False):
        print(f'File name: {file_info.file_name}, File ID: {file_info.id_}')

    # create a list of tuples with the file name and file id 
    file_names = [ (fi.file_name, fi.id_, format_timestamp(fi.upload_timestamp))for fi, fn in bucket_name.ls(show_versions=False)]

    return(file_names)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html', error_message='Page not found', error_code=404), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='Internal server error',error_code=500), 500

@app.route('/')
def home():
    return render_template("home.html", server_time=datetime.now().strftime('%I:%M %p'))

@app.route('/validate_ticket')
def working_page():
    event_id = request.args.get('event_id')
    ticket_id = request.args.get('ticket_id')

    if not event_id or not ticket_id:
        # Render the error.html template if parameters are missing
        return render_template('home.html')

    # Render the working.html template while working, passing event_id and ticket_id
    return render_template('loading.html', event_id=event_id, ticket_id=ticket_id)

@app.route('/submit', methods=['GET'])
def submit_request():
    now = datetime.now()
    scan_time = now.strftime(" %I:%M:%S %p | %Y-%m-%d")
    event_id = request.args.get('event_id')
    ticket_id = request.args.get('ticket_id') # ticket_id is the ticket_number - refactor ...
    
    if not event_id or not ticket_id:
            return Response("{'error': 'Missing event_id or ticket_id'}", status=400, mimetype='application/json')

    # read in the pickel file
    data = read_pickle(event_id)
    if data:
        webhook_url = data[0]['webhook_url']
        # subtract 1 because the fisrt entry is the webhook address
        data_len = len(data)-1
        # get the simple percentage of tickets scaned 
        percent_complete = (data_len/30) *100 if data_len >1 else 0
    else:
        return render_template('error.html', error_message='No Event data found', error_code=404), 404

    if data:
        # write - update data
        data[int(ticket_id)]['scan_time'] = scan_time
        data[int(ticket_id)]['percent_complete'] = percent_complete
        write_pickle(data, event_id)

    embed = {
        "title": "🚀",
        "description": f"Event ID: {event_id}\nTicket ID: {ticket_id}\nScan Time: {scan_time}\n\n{os.getenv('SERVER_URL')}",
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
    response = requests.post(webhook_url, json=payload)

    # Check the response
    if response.status_code == 204:
        print("Embed sent successfully!")
    else:
        print(f"Failed to send embed. Status code: {response.status_code} - Response: {response.text}")


    return render_template('verified.html', event_id=event_id, ticket_id=ticket_id, scan_time=scan_time, percent_complete=percent_complete)


        # # Get the current date and time, then subtract 3 hours  
        # now = datetime.now() - timedelta(hours=3)

        # # Target date and time for comparison
        # target_date_start = datetime.strptime(data[0]['event_date'], '%B %d %Y')
        # target_time_start = datetime.strptime(f"{data[0]['event_date']} {data[0]['event_start_time']}", 
        #                                     '%B %d %Y %I:%M %p')
        # target_time_end = target_time_start + timedelta(
        #                                             days = int(data[0]['event_duration']['days']), 
        #                                             hours = int(data[0]['event_duration']['hours']),
        #                                             minutes = int(data[0]['event_duration']['minutes'])
        #                                             )
        # logger.info(f"target_date_start: {type(target_date_start)}")
        # logger.info(f"target_time_start: {type(target_time_start)}")
        # logger.info(f"target_time_end: {type(target_time_end)}")

        # if now < target_date_start:
        #     # Calculate difference
        #     delta = now - target_date_start
        #     days = delta.days
        #     hours, remainder = divmod(delta.seconds, 3600)
        #     minutes, seconds = divmod(remainder, 60)
        #     logger.info(f"BEFORE - {days} days, {hours} hours and {minutes} minutes until the start")
        # elif now > target_time_end:
        #     logger.info("EVENT HAS HAPPENED")
        # else:
        #     if target_time_start <= now and now <= target_time_end: 
        #         # -------------------------- add validate code here [BEGIN]
        #         embed = {
        #             "title": "🚀",
        #             "description": f"Event ID: {event_id}\nTicket ID: {ticket_id}\nScan Time: {scan_time}\n\n{os.getenv('SERVER_URL')}",
        #             "color": 1543684, 
        #             "fields": [],
        #             "footer": {
        #                 "text": "** use report URL to get a text listing of all activity"
        #             }
        #         }

        #         # Wrap the embed in a payload as Discord expects
        #         payload = {
        #             "embeds": [embed],
        #         }

        #         # Convert the payload to JSON and make the POST request to the webhook URL
        #         response = requests.post(webhook_url, json=payload)

        #         # Check the response
        #         if response.status_code == 204:
        #             print("Embed sent successfully!")
        #         else:
        #             print(f"Failed to send embed. Status code: {response.status_code} - Response: {response.text}")


        #         return render_template('verified.html', event_id=event_id, ticket_id=ticket_id, scan_time=scan_time, percent_complete=percent_complete)
        #         # -------------------------- add validate code here [END]

        #         logger.log("HAPPENING")
        #     elif now < target_time_start:
        #         # Calculate difference
        #         delta = target_time_start - now
        #         hours, remainder = divmod(delta.seconds, 3600)
        #         minutes, seconds = divmod(remainder, 60)

        #         logger.log(f"{hours} hours and {minutes} minutes until the event")
        #     else:
        #         logger.log("EVENT HAS HAPPENED")







@app.route('/list_events', methods=['GET'])
def list_events_page():    
    # read in the pickel file
    data = list_bucket()
    
    return render_template('list_events.html', data=data)

@app.route('/list_event', methods=['GET'])
def list_event_page():
    event_id = request.args.get('event_id')

    # read in the pickel file
    data = read_pickle(event_id)
    percent_complete = (len(data) / 30) *100
    
    return render_template('list_event.html', data=data, percent_complete=percent_complete)



if __name__ == '__main__':
    app.run(debug=True)
