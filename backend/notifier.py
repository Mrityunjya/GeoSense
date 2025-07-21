from twilio.rest import Client

def send_sms_alert(message: str, to="+91xxxxxxxxxx"):
    account_sid = "your_sid"
    auth_token = "your_token"
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_="+1234567890",  # Your Twilio number
        to=to
    )
