import os, sys
import requests
import json
from dotenv import load_dotenv

os.chdir(os.path.join(str(os.getcwd())))

# Load environment variables
load_dotenv(".env")


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

def format_timestamp(timestamp):
    from datetime import datetime

    # Convert milliseconds to seconds
    timestamp_in_seconds = timestamp / 1000

    # Convert to a datetime object
    dt_object = datetime.fromtimestamp(timestamp_in_seconds)

    # Format the datetime object to a string in AM/PM format
    formatted_time = dt_object.strftime('%Y-%m-%d %I:%M:%S %p')

    return(formatted_time)

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


if __name__ =="__main__":

    # list_bucket()
    
    # test = {
    #     "one": [1,2,3],
    #     "two": {'A':1, "B":2,"C":3 }
    #     }

    # write_pickle_test(test, 'test_123')

    data = read_pickle('f_test_123')


    print()
    

