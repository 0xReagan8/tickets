import qrcode
import os

EVENT_ID="Some Event Title"
# format the event id so we can send in the URL
EVENT_ID= EVENT_ID.replace(' ', '_' )


# Ensure the directory for QR codes exists
output_dir = "qr_codes"
os.makedirs(output_dir, exist_ok=True)

base_url = "https://sore-cyan-ostrich-fez.cyclic.app/scan"  # Replace with your actual server address
# base_url = "https://sore-cyan-ostrich-fez.cyclic.app/scan?id="  # Replace with your actual server address
# base_url = "http://192.168.0.15:5900/scan?id="  # Replace with your actual server address

for i in range(1, 31):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    url = f"{base_url}?event_id={EVENT_ID}&ticket_id={i}"  # Added event_id to the URL

    print(url)

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code
    img.save(f"{output_dir}/QR_Code_{i}.png")

print("QR codes generated successfully.")
