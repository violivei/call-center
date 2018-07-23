import unittest
import mock

from app.call_handler import CallHandler
from app.call import Call
from app.respondent import Respondent


class CallTests(unittest.TestCase):
    def setUp(self):
        self.mock_call_handler = mock.create_autospec(CallHandler)
        self.mock_respondent = mock.create_autospec(Respondent)
        self.call_instance = Call(self.mock_call_handler)
        self.mock_respondent.rank = 0

    def tearDown(self):
        """
        This method is called after each tests
        """
        pass

    def test_set_respondent_handler_of_current_rank_or_higher(self):
        self.assertTrue(self.call_instance.set_respondent_handler(self.mock_respondent),msg='must be able to be associated with a call handler')
        self.call_instance.respondent_handler = None # reset call respondent

        self.mock_respondent.rank = 1
        self.assertTrue(self.call_instance.set_respondent_handler(self.mock_respondent),msg='must be able to be associated with a call handler greater than its own rank')
        return True

    def test_set_call_handler_below_rank(self):
        """
            must be not able to be associated with a call handler of lower rank
        """
        self.call_instance.rank = 1
        self.assertRaises(Exception, lambda: self.call_instance.set_respondent_handler(self.mock_respondent))
        return True

    def test_set_call_busy_handler(self):
        """  must be not able to be associated with a busy call handler """
        self.mock_respondent.is_free.return_value = False
        self.assertRaises(Exception, lambda: self.call_instance.set_respondent_handler(self.mock_respondent))
        return True

    def test_assign_to_free_respondent(self):
        self.mock_call_handler.dispatch_call.return_value = True
        self.assertTrue(self.call_instance.assign_to_free_respondent(),msg='must be capable of being assigned to free respondent')
        return True

    def test_assign_to_respondent_when_already_assigned(self):
        """  must be not able to be associated with a new respondent if call is already being handled """
        self.call_instance.set_respondent_handler(self.mock_respondent)
        self.assertRaises(Exception, lambda: self.call_instance.set_respondent_handler(self.mock_respondent))
        return True

    def test_assign_to_free_respondent_when_none_available(self):
        """ when all respondents are available, place call in queue """
        self.mock_call_handler.dispatch_call.return_value = False
        self.assertFalse(self.call_instance.assign_to_free_respondent(),msg='if no free respondents are available, add call to queue')
        return True

    def test_in_queue(self):
        self.mock_call_handler.call_queue = [self.call_instance]
        self.assertTrue(self.call_instance.in_queue(),msg='must return true when call is in queue')
        self.mock_call_handler.call_queue = []
        self.assertFalse(self.call_instance.in_queue(),msg='must return false when call is not in queue')
        return True

    def test_being_helped(self):
        self.call_instance.respondent_handler = None
        self.assertFalse(self.call_instance.being_helped(),msg='must return false when not being associated with respondent')
        self.call_instance.respondent_handler = self.mock_respondent
        self.assertTrue(self.call_instance.being_helped(),msg='must return true when being associated with respondent')
        return True


if __name__ == '__main__':
    unittest.main()


