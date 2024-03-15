![Alt text for the logo](/static/assets/logo_autonomous.svg)

# Tickets

## endpoints / routes


### /validate_ticket
*description:* 

- Sent from the QR code - contains the event and ticket information

*example:* 

    https://YOUR_URL.com/validate_ticket?event_id=test_123&ticket_id=5

<hr/>

### /list_events

*description:*

- Gets a list of all events recorded

*example:* 

    https://YOUR_URL.com/list_events

<hr/>


<hr/>

### /list_event

*description:*

- Gets the event records for the request event

*example:* 

    https://YOUR_URL.com/list_event?event_id=test_123

<hr/>


## generate events and tickets 

Note: The ticket generator uses [geckodriver](https://github.com/mozilla/geckodriver/releases) you can download it from this link.

1. create a .etc folder
2. Download gecko driver into ./etc/geckodriver
3. modify `./QR/assets/event_data.json` with your data
4. modify ./QR/generate_codes.py  `__main__` :
    
    - EVENET_ID = `"Your Event"`
    
    - NBR_CODE_TO_GENERATE = `YOUR_NUMBER_OF_TICKETS`

    - WEBHOOK_URL= `"YOUR_WEBHOOK_ADDRESS"`
