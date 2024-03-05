import qrcode
import os

# Ensure the directory for QR codes exists
output_dir = "qr_codes"
os.makedirs(output_dir, exist_ok=True)

base_url = "http://192.168.0.15:5900/scan?id="  # Replace with your actual server address

for i in range(1, 31):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    url = f"{base_url}{i}"
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code
    img.save(f"{output_dir}/QR_Code_{i}.png")

print("QR codes generated successfully.")


