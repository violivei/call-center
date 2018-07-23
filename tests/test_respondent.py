import unittest
import mock

from app.call_handler import CallHandler
from app.call import Call
from app.respondent import Respondent

""" TODO: Add some comments to this """


class RespondentTests(unittest.TestCase):
    def setUp(self):
        self.mock_call_handler = mock.create_autospec(CallHandler)
        self.mock_call = mock.create_autospec(Call)
        self.respondent = Respondent(self.mock_call_handler,'respondent')

    def tearDown(self):
        """
        This method is called after each tests
        """
        pass

    def test_set_respondent_type_verify_rank(self):
        self.respondent.set_respondent_type('respondent')
        self.assertEqual(self.respondent.rank,0,'Base Respondent should have rank 0')
        self.respondent.set_respondent_type('manager')
        self.assertEqual(self.respondent.rank,1,'Manager should have rank 1')
        self.respondent.set_respondent_type('director')
        self.assertEqual(self.respondent.rank,2,'Director should have rank 2')
        return True

    def test_set_respondent_type_verify_type_validity(self):
        """ If an invalid respondent type is passed to set_respondent_type should raise error """
        self.assertRaises(ValueError,lambda: self.respondent.set_respondent_type('bogus'))
        return True

    def test_recieve_call_when_free(self):
        self.assertTrue(self.respondent.recieve_call(self.mock_call))
        return True

    def test_recieve_call_when_not_free(self):
        self.respondent.recieve_call(self.mock_call)
        self.assertRaises(Exception,lambda: self.respondent.recieve_call(self.mock_call))
        return True

    def test_complete_call_when_not_free_side_effect(self):
        self.respondent.is_free = mock.Mock(return_value=True)
        with self.assertRaises(NameError) as cm:
            self.respondent.complete_call()
        return True

    def test_complete_call_when_not_free(self):
        self.respondent.recieve_call(self.mock_call)
        self.assertTrue(self.respondent.complete_call())
        return True

    def test_complete_call_when_free(self):
        self.assertRaises(NameError,lambda: self.respondent.complete_call())
        return True

    def test_escalate_and_reassign(self):
        self.respondent.recieve_call(self.mock_call)
        self.mock_call_handler.request_call_from_queue.return_value = self.mock_call
        self.assertTrue(self.respondent.escalate_and_reassign())
        self.assertEqual(self.respondent.call,self.mock_call)
        self.mock_call.increase_rank.assert_called_with()
        self.mock_call.assign_to_free_respondent.assert_called_with()
        return True

    def test_assign_new_call(self):
        self.mock_call_handler.request_call_from_queue.return_value = self.mock_call
        self.respondent.assign_new_call()
        self.mock_call_handler.request_call_from_queue.assert_called_with(self.respondent.rank)
        self.mock_call.set_respondent_handler.assert_called_with(self.respondent)
        return True

    def test_is_free(self):
        self.assertTrue(self.respondent.is_free())
        self.respondent.assign_new_call(self.mock_call)
        self.assertFalse(self.respondent.is_free())
        return True


if __name__ == '__main__':
    unittest.main()

