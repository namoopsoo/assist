
import settings

class ServerResponder(object):
    UNKNOWN_SENDER_REPLY = 'Unknown sender. Please register.'
    UNKNOWN_COMMAND_REPLY = 'Unknown command, but thanks.'

    def __init__(self, request):
        self.request = request


    def handle_message(self):
        '''Handles a Flask request  from twilio '''

        # Quit out if unknown sender
        recognized_caller = self.check_if_recognized_caller()
        if not recognized_caller:
            reply = self.UNKNOWN_SENDER_REPLY 
            resp = self.form_twiml_reply(reply)
            return resp

        # Try to determine Action
        result = self.determine_action_from_request()
        if not result:
            reply = self.UNKNOWN_COMMAND_REPLY
            resp = self.form_twiml_reply(reply)


        reply = self.get_command_reply(command)

        resp = self.form_twiml_reply(reply)
        return str(resp)

    def check_if_recognized_caller(self):
        from_number = self.request.get('From', None)
        if from_number in settings.CALLERS:
            return True
        else:
            return False

    def determine_action_from_request(self):
        '''See if valid action from message'''

        body = self.request.get('Body')

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
 

