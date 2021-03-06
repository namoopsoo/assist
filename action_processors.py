
import httplib2
import os
import datetime

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from quickstart_google_cal import get_credentials


from utils import send_message

class Action(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.command = kwargs['command']
        self.content_dict = kwargs['content_dict']
        self.raw_content = kwargs['raw_content']
        self.originator = kwargs['originator']

class ActionProcessor(object):
    NEXTEVENT = 'nextevent'

    def __init__(self, action, **kwargs):
        self.action = action

    def send_the_reply(self, reply):
        ''' Perform the reply send.
        '''
        to_num = '+1{number}'.format(
                number=self.action.originator['number'])

        send_message(to=to_num, body=reply)


class CalendarActionProcessor(ActionProcessor):

    def __init__(self, action, **kwargs):
        #
        super(CalendarActionProcessor, self).__init__(action, **kwargs)

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def process_reply(self):
        ''' Process action and send back reply
        '''
        self.action

        next_event = self.get_next_cal_event()
        if not next_event:
            return None

        originator_name = self.action.originator['name']

        reply = 'Hi {name}, {action_name} result: {result}'.format(
                name=originator_name,
                action_name=self.action.name,
                result=next_event)

        self.send_the_reply(reply)

    def get_next_cal_event(self):

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print 'Getting the upcoming 10 events'
        eventsResult = self.service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if events:
            print 'No upcoming events found.'
            next_event = events[0]

            start = next_event['start'].get('dateTime', next_event['start'].get('date'))
            event_text = '{}, {}'.format(start, next_event['summary'])
            return event_text
        else:
            return None
