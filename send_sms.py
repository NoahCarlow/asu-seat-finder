# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Account Sid and Auth Token from twilio.com/console
# Currently not use environmental variables but definetly should
account_sid = "Account SID"
auth_token = "Account Token"
client = Client(account_sid, auth_token)