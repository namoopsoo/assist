
import re

from action_processors import Action
from tasks import process_actions
from utils import form_twiml_reply

import settings

class ServerResponder(object):
    UNKNOWN_SENDER_REPLY = 'Unknown sender. Please register.'
    UNKNOWN_COMMAND_REPLY = 'Unknown command, but thanks.'
    THANKS_FOR_MESSAGE_REPLY = 'Thanks for _{action_name}_ message, {name}. '

    def __init__(self, request):
        self.request = request

    def handle_message(self):
        '''Handles a Flask request  from twilio '''

        # Quit out if unknown sender
        caller_dict = self.get_caller()
        if not caller_dict:
            reply = self.UNKNOWN_SENDER_REPLY
            resp = form_twiml_reply(reply)
            return resp

        # Try to determine Action
        action = self.determine_action_from_request()
        if not action:
            reply = self.UNKNOWN_COMMAND_REPLY
            resp = form_twiml_reply(reply)
            return resp

        # Absorb caller
        action.originator = caller_dict

        #
        # Until queueing the actions in a rabbit mq, just call process_actions() outright.
        # This will also send replies ( out of order however, for now).
        actions = [action]
        process_actions(actions)

        reply = self.get_acknowledgement_reply(action)
        resp = form_twiml_reply(reply)
        return str(resp)

    def get_caller(self):
        raw_number = self.request.get('From', None)

        m = re.match('\+1(\d*)$', raw_number)
        try:
            from_number = m.group(1)
        except IndexError:
            return None
        caller_dict = settings.CALLERS.get(from_number)
        if not caller_dict: 
            return None

        caller_dict['number'] = from_number
        return caller_dict

    def determine_action_from_request(self):
        '''See if valid action from message'''
        body = self.request.get('Body')
        action = None

        legal_actions = {
            'nextevent': 1,
            'co robisz': 1,
            'gdzie jestes': 1,
        }

        for command_ in legal_actions.keys():
            match = re.match(command_ + '(.*)$', body)
            if match:
                content = match.groups()
                content = content[0]

                action = Action(
                        name='nextevent',
                        command='nextevent',
                        raw_content=content,
                        content_dict={},
                        originator=None,
                        )
                break

        return action

    def get_acknowledgement_reply(self, action):
        ''' After queueing the action, acknowledge its receipt.
        '''
        caller_name = action.originator['name']
        action_name = action.name

        response = self.THANKS_FOR_MESSAGE_REPLY.format(name=caller_name,
                action_name=action_name)

        return response

