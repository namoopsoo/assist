from flask import Flask, request, redirect
import twilio.twiml

# from quickstart_google_cal import MyCalendar
from responder import ServerResponder
from utils import form_twiml_reply


import settings
 
app = Flask(__name__)
 
@app.route("/reply", methods=['GET', 'POST'])
def main_twilio_entrypoint():

    import pdb; pdb.set_trace()
    r = ServerResponder(request.values)

    reply = r.handle_message()

    # response = form_twiml_reply(reply)
    # return response
    return reply


if __name__ == "__main__":
    app.run(debug=True)

