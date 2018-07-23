from .call_handler import CallHandler
from .respondent import Respondent


class Call:
    """
    rank - the minimum level of an respondent who can handle the call
    respondent - the respondent handling the call
    resolved - has the issue been resolved by an respondent?
    """

    def __init__(self, call_handler):
        self.rank = 0
        self.respondent_handler = None
        self.set_call_handler(call_handler)
        self.resolved = False

    def set_call_handler(self, call_handler):
        """ associate with call handler queue return true if successful """

        if isinstance(call_handler, CallHandler):
            self.call_handler = call_handler
            return True
        else:
            raise TypeError('call handler queue can only handle valid calls')

    def set_respondent_handler(self, respondent):
        """
        associate with an respondent of the call center
        if the respondent is of rank below the rank of the call, raise error
        if the respondent is of rank >= rank of call, return True
        """
        if not self.being_helped():
            if isinstance(respondent, Respondent) and respondent.is_free():
                if respondent.rank >= self.rank:
                    self.respondent_handler = respondent
                    return True
                else:
                    raise TypeError('call must be handled by an respondent of >= rank')
            else:
                raise TypeError('call must be handled by a free respondent')
        else:
            raise Exception('can only be handle by one respondent at a time.')

    def assign_to_free_respondent(self):
        """
        make an attempt to associate call with any available call center respondent.
        if none available, place in queue
        """
        respondent = self.call_handler.dispatch_call(self)
        if respondent:
            return True

    def in_queue(self):
        """  am I currently in a queue? """
        if self in self.call_handler.call_queue:
            return True

    def being_helped(self):
        """  am I currently being helped by a call center respondent? """
        if self.respondent_handler is not None:
            return True

    def in_queue_or_being_helped(self):
        if self.in_queue() or self.being_helped():
            return True

    def increase_rank(self):
        self.rank += 1
        return self.rank

    def disconnect(self):
        self.resolved = True
        self.call_handler.remove_call_from_queue(self)
