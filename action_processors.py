
class Action(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.command = kwargs['command']
        self.content_dict = kwargs['content_dict']

class ActionProcessor(object):
    def get_command_reply(self, command):

        if command == 'nextevent':    

            my_calendar = MyCalendar()
            next_event = my_calendar.get_next_cal_event()
            if next_event:
                return next_event

        return 'foo'

class CalendarActionProcessor(ActionProcessor):

    def __init__(self):
        #
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

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
