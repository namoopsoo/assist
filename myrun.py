from flask import Flask, request, redirect
import twilio.twiml

from responder import ServerResponder

 
app = Flask(__name__)
 
@app.route("/reply", methods=['GET', 'POST'])
def main_twilio_entrypoint():
    r = ServerResponder(request.values)
    reply = r.handle_message()
    return reply


if __name__ == "__main__":
    app.run(debug=True)

