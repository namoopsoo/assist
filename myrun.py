from flask import Flask, request, redirect
import twilio.twiml

from quickstart_google_cal import MyCalendar
from responder import ServerResponder

import settings
 
app = Flask(__name__)
 
@app.route("/reply", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    r = ServerResponder()
 
    from_number = request.values.get('From', None)

    recognized_caller = check_if_recognized_caller(from_number)
    if recognized_caller:
        command = get_command_from_request(request)
        if command:
            reply = get_command_reply(command)
        else:
            reply = 'Unknown command, but have a nice day!'
    else:
        reply = 'Unknown sender. Please register.'

    resp = form_reply(reply)
    return str(resp)

def form_reply(reply_text):
    resp = twilio.twiml.Response()
    resp.message(reply_text)

    return resp


def check_if_recognized_caller(from_number):
    if from_number in settings.CALLERS:
        return True
    else:
        return False

def get_command_from_request(request):
    body = request.values.get('Body')

    words = body.split(' ')

    legal_commands = {
        'nextevent': 1
    }

    command = None

    if words:
        first_word = words[0]
        if first_word in legal_commands:
            command = first_word

    return command
 
def get_command_reply(command):

    if command == 'nextevent':    

        my_calendar = MyCalendar()
        next_event = my_calendar.get_next_cal_event()
        if next_event:
            return next_event

    return 'foo'


if __name__ == "__main__":
    app.run(debug=True)
