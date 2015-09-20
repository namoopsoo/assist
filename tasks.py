

from action_processors import ActionProcessor, CalendarActionProcessor

def process_actions(actions):
    ''' For queued actions, determine and call the appropriate ActionProcessor
    '''

    for action in actions:
        if action.command == ActionProcessor.NEXTEVENT:
            processor = CalendarActionProcessor(action)

            processor.process_reply()

    pass

