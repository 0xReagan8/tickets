import os
import json
import base64
from colorama import Fore, Style
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


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

def render_tickets():
    print(f""" 
    {Fore.LIGHTGREEN_EX} 🐟🐟 rendering tickets: {Style.RESET_ALL}
    """)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load event data
    with open(os.path.join(assets_dir, 'event_data.json'), 'r') as file:
        event_data = json.load(file)

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
                event_title=event_data['event_name'],
                event_date=event_data['event_date'],
                event_time=event_data['event_time']
            )
            # Define output filenames
            base_filename = qr_code_file.split('.')[0]
            html_filename = os.path.join(output_dir, f'{base_filename}.html')
            pdf_filename = os.path.join(output_dir, f'{base_filename}.pdf')
            png_filename = os.path.join(output_dir, f'{base_filename}.png')

            # Save the rendered HTML
            with open(html_filename, 'w') as file:
                file.write(rendered_html)

            # Convert HTML to PDF using WeasyPrint
            HTML(string=rendered_html, base_url=output_dir).write_pdf(pdf_filename)

            # Convert HTML to PNG using Selenium
            driver.get(f'file://{html_filename}')
            driver.set_window_size(1200, 800)  # Adjust as needed
            driver.save_screenshot(png_filename)

    driver.quit()
    print(f""" 
    {Fore.WHITE} 🦞 Processing complete 🦞... {Style.RESET_ALL} 
    """)
