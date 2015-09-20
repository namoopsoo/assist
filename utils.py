

import twilio.twiml
from twilio.rest import TwilioRestClient

import settings

def form_twiml_reply(reply_text):


    resp = twilio.twiml.Response()
    resp.message(reply_text)

    resp_str = str(resp)

    return resp_str

def send_message(to, body):
    '''
    Download the twilio-python library from http://twilio.com/docs/libraries

    # Find these values at https://twilio.com/user/account
    '''
    ENDPOINT = 'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages'.format(
            account_sid=settings.ACCOUNT_SID)

    client = TwilioRestClient(account=settings.ACCOUNT_SID,
                            token=settings.AUTH_TOKEN,
                            base=settings.TWILIO_API_URL_BASE,
                            version=settings.TWILIO_API_URL_VERSION)

    message = client.messages.create(to=to, from_=settings.TWILIO_FROM_NUM,
                                     body=body)

    # Expecting a reply to this message?
    message_sid = message.sid
    print message_sid
    

