        
import requests
import json

# Your Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1214662183452016660/1yOSpSVg3oj0gr6rQWnpKW9ncjt-TKeODdlzXE12hWSLwmNlUNOEUI21L3hmxPYCvK5u"


embed = {
    "title": "🚀",
    "description": "Event ID: <EVENT ID>\nTicket ID: <TICKET ID>\nScan Time: <SCAN TIME>\n\nhttps://sore-cyan-ostrich-fez.cyclic.app",
    "color": 1543684, 
    "fields": [],
    "footer": {
        "text": "** use report URL to get a text listing of all activity"
    }
}

# Wrap the embed in a payload as Discord expects
payload = {
    "embeds": [embed],
}

# Convert the payload to JSON and make the POST request to the webhook URL
response = requests.post(webhook_url, json=payload)

# Check the response
if response.status_code == 204:
    print("Embed sent successfully!")
else:
    print(f"Failed to send embed. Status code: {response.status_code} - Response: {response.text}")
