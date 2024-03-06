import qrcode
import os

EVENT_ID="Some Event Title"
# format the event id so we can send in the URL
EVENT_ID= EVENT_ID.replace(' ', '_' )


# Ensure the directory for QR codes exists
output_dir = "qr_codes"
os.makedirs(output_dir, exist_ok=True)

base_url = "https://sore-cyan-ostrich-fez.cyclic.app/scan"  # Replace with your actual server address
# base_url = "192.168.0.15:5800/scan"  # Replace with your actual server address

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


# https://sore-cyan-ostrich-fez.cyclic.app/scan?event_id=Some_Event_Title&ticket_id=5
# https://sore-cyan-ostrich-fez.cyclic.app/scan?event_id=Some_Event_Title&ticket_id=6


https://sore-cyan-ostrich-fez.cyclic.app
Get an item: curl -i -XGET https://sore-cyan-ostrich-fez.cyclic.app/item/1

Get an item: curl -i -XGET http://localhost:8181/item/1

List items: curl -i -XGET http://localhost:8181/items/

Post an item: curl -i -XPOST http://localhost:8181/items/ --data '{"item_id":1,"name":"Bob"}' -H 'content-type: application/json'

