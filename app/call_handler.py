class CallHandler:
    """
    The main class. Handles the associating respondents with calls, redirecting calls to a queue if respondent is unavailable
    """

    def __init__(self):
        self.respondent_types = ["respondent", "manager", "director"]
        self.call_queue = []
        self.respondents = []

    def add_respondent(self, respondent):
        self.respondents.append(respondent)

    def locate_handler_for_call(self, rank):
        """
        Get the first respondent available who can handle the call of a specific rank
        """

        if type(rank) is not int:
            raise TypeError('Rank must be an integer')

        """ might want to rework this, it should stop after finding first available respondent """
        available_respondents = list(filter(lambda x: x.is_free() and x.rank == rank, self.respondents))
        if len(available_respondents) > 0:
            return available_respondents[0]

    def dispatch_call(self, call):
        """
        routes the call to an available respondent of appropriate rank, otherwise places call in a queue if no one is available
        """

        if call.resolved:
            return False
        emp = self.locate_handler_for_call(call.rank)
        if emp:
            emp.assign_new_call(call)
            return emp
        else:
            if call not in self.call_queue:
                self.call_queue.append(call)
                return False

    def request_call_from_queue(self, rank):
        """
        return any available calls that are queued at the rank specified
        """
        if type(rank) is not int:
            raise TypeError('rank must be an integer')

        queued_calls = list(filter(lambda x: x.rank == rank and x.resolved != True and x.being_helped() != True, self.call_queue))
        if len(queued_calls) > 0:
            return queued_calls[0]

    def remove_call_from_queue(self, call):
        if call.resolved:
            self.call_queue.remove(call)
