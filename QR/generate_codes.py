import os
import pickle
import qrcode
import render_qr_codes
from colorama import Fore, Style
from dotenv import load_dotenv

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

def generate_QR_codes(event_id, number_to_generate):
    # Ensure the directory for QR codes exists
    output_dir = "qr_codes"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, number_to_generate+1):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        url = f"{BASE_URL}?event_id={event_id}&ticket_id={i}"  # Added event_id to the URL

        print(f""" 
        {Fore.LIGHTBLACK_EX} 🐟 rendering ticket: {i} {Style.RESET_ALL}
        {Fore.LIGHTCYAN_EX} 🐠🐠 encoded URL: {Style.RESET_ALL} {url} {Fore.WHITE} {Style.RESET_ALL}
        """) 

        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        img.save(f"{output_dir}/QR_Code_{i}.png")

    print("QR codes generated successfully.")

def main(event_id, webhook_url, nbr_codes_to_generate):
    # format the event id
    event_id = format_event_id(EVENET_ID)

    # test is the pickle file exist
    if not read_pickle(event_id):
        # the pickle file does not exist - create an empty one
        # the first entry has the webhook url of the discord server
        write_pickle({"webhook_url":webhook_url}, event_id)

    generate_QR_codes(event_id, nbr_codes_to_generate)


if __name__ == "__main__":
    # add your event name here
    EVENET_ID = "Test Event 5"

    # add your total number of event tickets here
    NBR_CODE_TO_GENERATE = 5

    # add your discord server webhook here
    WEBHOOK_URL="https://discord.com/api/webhooks/1215792940664881172/iisvqo4MRKvnqRyW9Xq6I92ZOU0KwMrYAILoLAYjjUhkQNt7VYpOoDkliAgKb-638onS"

    # generate the codes
    main(EVENET_ID, WEBHOOK_URL, NBR_CODE_TO_GENERATE)

    # render the tickets
    render_qr_codes.render_tickets()
    
