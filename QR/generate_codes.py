import sys
import os
import shutil
import qrcode
import render_qr_codes
from datetime import datetime, timezone
from colorama import Fore, Style
from dotenv import load_dotenv
import uuid

sys.path.append(os.getcwd())

from storage.cloudStorage import B2Storage
from sendOwl.sendOwlProduct import SendOwlProduct

os.chdir(os.path.join(str(os.getcwd())))

# Load environment variables
load_dotenv(".env")

SERVER_URL = "https://dull-tan-hatchling-cap.cyclic.app"
ENDPOINT = "validate_ticket"
BASE_URL = f"{SERVER_URL}/{ENDPOINT}"  # Replace with your actual server address


def write_pickle(data:dict, event_id:str):
    import io
    import pickle
    import json
    from b2sdk.v1 import InMemoryAccountInfo, B2Api

    # dump to a bstrt
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
    print(f"Data uploaded to file {file_name} with version {b2_file_version.id_}")

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

    # File to download
    file_name = f'{event_id}.pck'  # The name of the file in B2

    try:
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

def format_event_id(event_id):
    # format the event id so we can send in the URL
    event_id_formatted =  event_id.replace(' ', '_' ).lower()

    return(event_id_formatted)

def generate_QR_codes(event_name, event_location, event_date, event_time, event_price, nbr_codes_to_generate, webhook_url):
    # Ensure the directory for QR codes exists
    output_dir = "qr_codes"
    ticket_output_dir="/home/sbellina/jobs/tickets/tickets_output/"
    os.makedirs(output_dir, exist_ok=True)

    # remove old generated codes
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    # dictionary to hold upload and rendering data
    data = []

    for i in range(1, nbr_codes_to_generate+1):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        url = f"{BASE_URL}?event_id={event_name}&ticket_id={i}"  # Added event_id to the URL

        print(f""" 
        {Fore.LIGHTBLACK_EX} 🐟 rendering ticket: {i} {Style.RESET_ALL}
        {Fore.LIGHTCYAN_EX} 🐠🐠 encoded URL: {Style.RESET_ALL} {url} {Fore.WHITE} {Style.RESET_ALL}
        """) 

        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        img.save(f"{output_dir}/QR_Code_{i}.png")

        data.append(
            {
                'id':uuid.uuid4(), 
                'ticket_number':i, 
                'event_id':event_name,
                'event_location':event_location,
                'event_date':event_date,
                'event_time':event_time,
                'event_price':event_price,
                'attachment':os.path.join(ticket_output_dir, f"QR_Code_{i}.pdf"),
                'created_at':datetime.now(timezone.utc),
                'webhook_url':webhook_url
                    }
        )

    print("QR codes generated successfully.")
    return(data)

def main(event_name, event_location, event_date, event_time, event_price, webhook_url, nbr_codes_to_generate):
    # format the event id
    event_name = format_event_id(EVENET_NAME)

    # # test is the pickle file exist
    # if not B2Storage.read_pickle(event_name):
    #     # the pickle file does not exist - create an empty one
    #     # the first entry has the webhook url of the discord server
    #     B2Storage.write_pickle({"webhook_url":webhook_url}, event_name)
        
    # generate the codes and product data
    # NOTE: product data genetred is used to sendOwl 
    product_data = generate_QR_codes(event_name, event_location, event_date, event_time, event_price, nbr_codes_to_generate, webhook_url)

    try:    
        # write the product data to storage
        B2Storage.write_pickle(product_data, event_name)
    except Exception as e:
        print(f"""💩{Fore.LIGHTRED_EX} ERR: cold not write to storage: {Style.RESET_ALL}
              {Fore.LIGHTBLACK_EX} {e} {Style.RESET_ALL} 
              💩""")

    # render the tickets
    render_qr_codes.render_tickets(event_name, event_location, event_date, event_time)

    # if not DEBUG_MODE:
    #     #create the sendOwl Product object
    #     sendOwlProduct = SendOwlProduct()

    #     for data in product_data:
    #         sendOwlProduct.create_product(data)

    print()


if __name__ == "__main__":
    # for testing  - if true  - products are not sent to sendOwl
    DEBUG_MODE=False

    # add your event name here
    EVENET_NAME = "CLASSIC PUNK PARTY" 
    # add your event's location address here
    EVENT_LOCATION = "Otra Historia, Estomba 851"
    # add your date
    EVENT_DATE = "March 16 2024"
    # add your time
    EVENT_TIME = "6:00 PM - 6:00 AM"
    # add your total number of event tickets here
    EVENT_PRICE=10.00

    NBR_CODE_TO_GENERATE = 2

    # add your discord server webhook here
    WEBHOOK_URL="https://discord.com/api/webhooks/1215792940664881172/iisvqo4MRKvnqRyW9Xq6I92ZOU0KwMrYAILoLAYjjUhkQNt7VYpOoDkliAgKb-638onS"

    # generate the codes
    main(EVENET_NAME, EVENT_LOCATION, EVENT_DATE, EVENT_TIME, EVENT_PRICE, WEBHOOK_URL, NBR_CODE_TO_GENERATE)
