import os
import shutil
import json
import base64
from colorama import Fore, Style
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from PIL import Image
import uuid



# Set the paths
base_dir = os.path.abspath('QR')
assets_dir = os.path.join(base_dir, 'assets')
templates_dir = os.path.join(base_dir, 'templates')

qr_codes_dir = os.path.abspath('qr_codes')
output_dir = os.path.abspath('tickets_output')

def image_to_base64(image_path):
    print(f""" {Fore.LIGHTYELLOW_EX} converting file: {Style.RESET_ALL} {Fore.YELLOW} image_path to base64 {Style.RESET_ALL}""")

    _, file_extension = os.path.splitext(image_path)
    if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f'data:image/{file_extension[1:]};base64,{encoded_string}'
    elif file_extension.lower() == '.svg':
        with open(image_path, 'r') as image_file:
            return image_file.read()

def render_tickets(event_name, event_location, event_date, event_time):
    print(f""" 
    {Fore.LIGHTGREEN_EX} 🐟🐟 rendering tickets: {Style.RESET_ALL}
    """)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('event_ticket_template.html')

    # Specify the path to the geckodriver executable
    geckodriver_path = './etc/geckodriver'  # Ensure this path is correct

    # Set Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")

    # Initialize the Firefox WebDriver with the specified options
    driver = webdriver.Firefox(service=Service(executable_path=geckodriver_path), options=firefox_options)

    # Process each QR code
    for qr_code_file in os.listdir(qr_codes_dir):
        if qr_code_file.endswith('.png'):
            print(f""" 
            {Fore.LIGHTBLUE_EX} 🐡 rendering ticket: {Style.RESET_ALL} {Fore.CYAN} {qr_code_file} {Style.RESET_ALL}
            """)

            # Render the HTML with the QR code and event data using Base64 encoded images
            rendered_html = template.render(
                bg_image=image_to_base64(os.path.join(assets_dir, 'bg.png')),
                logo_image=image_to_base64(os.path.join(assets_dir, 'logo_autonomous.svg')),
                qr_code_image=image_to_base64(os.path.join(qr_codes_dir, qr_code_file)),
                event_logo=image_to_base64(os.path.join(assets_dir, 'event_logo.png')),                
                event_title=event_name,
                event_location=event_location,
                event_date=event_date,
                event_time=event_time,
                lion_lock_code=uuid.uuid4()
            )
            # Define output filenames
            base_filename = qr_code_file.split('.')[0]
            html_filename = os.path.join(output_dir, f'{base_filename}.html')
            pdf_filename = os.path.join(output_dir, f'{base_filename}.pdf')
            png_filename = os.path.join(output_dir, f'{base_filename}.png')

            # Save the rendered HTML
            with open(html_filename, 'w') as file:
                file.write(rendered_html)

            # Convert HTML to PNG using Selenium
            driver.get(f'file://{html_filename}')
            driver.set_window_size(820, 1180)  # Adjust as needed
            driver.save_screenshot(png_filename)

            # Convert PNG to PDF
            image = Image.open(png_filename)
            image.convert('RGB').save(pdf_filename, 'PDF')

    driver.quit()

    print(f""" 

    {Fore.WHITE} 🦞 Processing complete 🦞... {Style.RESET_ALL} 

    """)
    