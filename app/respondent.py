class Respondent:
    def __init__(self, call_handler, respondent_type='respondent'):
        self.set_call_handler(call_handler)
        self.set_respondent_type(respondent_type)
        self.call = None

    def set_call_handler(self, call_handler):
        self.call_handler = call_handler
        self.call_handler.add_respondent(self)

    def set_respondent_type(self, respondent_type):
        respondent_types = ["respondent", "manager", "director"]
        if respondent_type in respondent_types:
            for i, j in enumerate(respondent_types):
                if j == respondent_type:
                    self.rank = i
        else:
            raise ValueError('Rank of respondent must in ["respondent", "manager", "director"]')

    def recieve_call(self, call):
        if self.is_free():
            self.call = call
            return True
        else:
            raise Exception('can only be on one call at a time')

    def complete_call(self):
        """
        disconnect the current call, set current call to null
        if no current call if available, raise error
        """
        if not self.is_free():
            self.call.disconnect()
            self.call = None
            return True
        else:
            raise NameError('Instance not currently associated with a valid call')

    def escalate_and_reassign(self):
        """
            escalate the level of the current call, grab a new call from the queue
        """
        if not self.is_free():
            self.call.increase_rank()
            self.call.assign_to_free_respondent()
            self.call = None
            self.assign_new_call()
            return True
        else:
            raise NameError('Instance not currently associated with a valid call')

    def assign_new_call(self, call=None):
        """
            grab a new call from the queue at my current level
        """
        if self.is_free():
            if not call:
                call = self.call_handler.request_call_from_queue(self.rank)

            if call:
                call.set_respondent_handler(self)
                self.call = call

        else:
            raise NameError('Instance is currently associated with a valid call')

    def is_free(self):
        if self.call is None:
            return True