import unittest
from app.call_handler import CallHandler
from app.call import Call
from app.respondent import Respondent


class RespondentTests(unittest.TestCase):
    """This is a first attempt at integration tests. Should be refactored,mocking is a better approach"""

    def setUp(self):
        """
        This method is called before each tests
        """
        self.call_handler = CallHandler()
        self.emp = Respondent(self.call_handler, 'respondent')
        self.call_instance = Call(self.call_handler)
        self.call_instance_two = Call(self.call_handler)
        self.call_instance_three = Call(self.call_handler)
        self.call_handler.call_queue = [self.call_instance, self.call_instance_two, self.call_instance_three]

    def tearDown(self):
        """
        This method is called after each tests
        """
        pass

    def test_complete_call(self):
        self.assertTrue(self.emp.is_free(), msg='respondent should be free before proceeding')
        self.emp.recieve_call(self.call_instance)
        self.emp.complete_call()
        self.assertTrue(self.emp.is_free(), msg='respondent does not appear to be free')
        return True

    def test_complete_call_when_call_is_undefined(self):
        """ shouldnt be able to complete a call that doesnt exist """
        self.assertRaises(NameError, lambda: self.emp.complete_call())
        return True

    def test_escalate_and_reassign_when_call_is_not_undefined(self):
        """ verify escalate_and_reassign. existing call should be escalated to higher level, new call should be reassigned """
        self.emp.recieve_call(self.call_instance)
        self.call_instance_two.assign_to_free_respondent()
        self.assertTrue(self.emp.escalate_and_reassign())
        self.assertTrue(self.call_instance.in_queue_or_being_helped(), msg='existing call not in queue or being helped')
        self.assertEqual(self.call_instance.rank, 1, msg='existing call not being escalated')
        self.assertFalse(self.emp.is_free(), msg='respondent should be assigned to new call')
        return True

    def test_escalate_and_reassign_when_call_is_undefined(self):
        """ shouldnt be able to escalate_and_reassign when not in call """
        self.assertRaises(NameError, lambda: self.emp.escalate_and_reassign())
        return True

    def test_assign_new_call_when_call_is_not_undefined(self):
        """ shouldnt be able to assign new call when in current call """
        self.emp.recieve_call(self.call_instance)
        self.assertRaises(NameError, lambda: self.emp.assign_new_call(self.call_instance))
        return True


class CallHandlerTests(unittest.TestCase):
    def setUp(self):
        """
        This method is called before each tests
        """
        self.call_handler = CallHandler()
        self.respondent = Respondent(self.call_handler, 'respondent')
        self.respondent_b = Respondent(self.call_handler, 'respondent')
        self.manager = Respondent(self.call_handler, 'manager')
        self.director = Respondent(self.call_handler, 'director')

        self.call_instance = Call(self.call_handler)
        self.call_instance_two = Call(self.call_handler)
        self.call_instance_three = Call(self.call_handler)

    def tearDown(self):
        """
        This method is called after each tests
        """
        pass

    def test_locate_handler_rank_all_respondents_available(self):
        self.assertEqual(self.call_handler.locate_handler_for_call(0), self.respondent, msg='Not being directed towards available respondent rank 0')
        self.assertEqual(self.call_handler.locate_handler_for_call(1), self.manager, msg='Not being directed towards available respondent rank 1')
        self.assertEqual(self.call_handler.locate_handler_for_call(2), self.director, msg='Not being directed towards available respondent rank 2')
        return True

    def test_call_and_respondent_assignment(self):
        self.respondent.assign_new_call(self.call_instance)
        self.assertEqual(self.call_instance.respondent_handler, self.respondent, msg='Call is not being correctly associated with a user')
        return True

    def test_locate_handler_rank_respondents_busy(self):
        self.respondent.assign_new_call(self.call_instance)
        self.assertEqual(self.call_handler.locate_handler_for_call(0), self.respondent_b, msg='Not being directed towards available next respondent rank 0')
        self.respondent_b.assign_new_call(self.call_instance_two)
        self.assertFalse(self.call_instance_three.assign_to_free_respondent(), msg='Should not have been passed an respondent')
        self.assertEqual(self.call_handler.request_call_from_queue(0), self.call_instance_three, msg='Not being passed the first available call from the queue')
        return True


if __name__ == '__main__':
    unittest.main()
