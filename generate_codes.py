import qrcode
import os

SERVER_URL = "https://dull-tan-hatchling-cap.cyclic.app"
ENDPOINT = "validate_ticket"
BASE_URL = f"{SERVER_URL}/{ENDPOINT}"  # Replace with your actual server address


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

        url = f"{BASE_URL}?event_id={EVENT_ID}&ticket_id={i}"  # Added event_id to the URL

        print(url)

        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        img.save(f"{output_dir}/QR_Code_{i}.png")

    print("QR codes generated successfully.")

if __name__ == "__main__":

    # add your event name here
    EVENET_ID = "Test Event 2"
    # add your totoal number of event tickets here
    NBR_CODE_TO_GENERATE = 30

    event_id = format_event_id(EVENET_ID)
    generate_QR_codes(event_id, NBR_CODE_TO_GENERATE)