import os
import io
import pickle
from b2sdk.v1 import InMemoryAccountInfo, B2Api, DownloadDestBytes
from dotenv import load_dotenv

os.chdir(os.path.join(str(os.getcwd())))

# Load environment variables
load_dotenv(".env")



class B2Storage:
    @staticmethod
    def write_pickle(data:dict, event_id:str):

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

    @staticmethod
    def read_pickle(event_id):
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
