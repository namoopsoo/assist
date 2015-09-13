from flask import Flask, request, redirect
import twilio.twiml

from quickstart_google_cal import MyCalendar
from responder import ServerResponder

import settings
 
app = Flask(__name__)
 
@app.route("/reply", methods=['GET', 'POST'])
def main_twilio_entrypoint():

    import pdb; pdb.set_trace()
    r = ServerResponder(request.values)

    reply = r.handle_message()

    response = form_twiml_reply(reply)
    return response

def form_twiml_reply(reply_text):
    resp = twilio.twiml.Response()
    resp.message(reply_text)

    return resp

if __name__ == "__main__":
    app.run(debug=True)

