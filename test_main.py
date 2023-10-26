import unittest
from unittest.mock import Mock, patch
patch('firebase_functions.scheduler_fn.on_schedule', lambda schedule, region : (lambda x : x)).start()
from functions.main import last_word, daily_word

class mock__Request():
   method = ""
   class args():
    word = None
    def get(self):
        return mock__Request.args.word

class TestCloudFunction(unittest.TestCase):

    @patch('firebase_admin.firestore.client')
    def test_daily_word(self, mock):
        daily_word(Mock())
        mock.return_value.collection.return_value.document.return_value.set.assert_called()

    def test_options(self):
        req=mock__Request
        req.method="OPTIONS"
        cloud_func = last_word(request=req)
        self.assertEqual(cloud_func.status_code, 204, 'Test pre-flight')

    @patch('firebase_admin.firestore.client')
    def test_get_noInput(self, mock):
        req=mock__Request
        req.method="GET"
        mock__Request.args.word = None
        cloud_func = last_word(request=req)
        self.assertEqual(cloud_func.status_code, 200, 'Test get')
        mock.return_value.collection.return_value.document.return_value.set.assert_not_called()

    @patch('firebase_admin.firestore.client')
    def test_get_input(self, mock):
        req=mock__Request
        req.method="GET"
        mock__Request.args.word="hi"
        cloud_func = last_word(request=req)
        self.assertEqual(cloud_func.status_code, 200, 'Test get')
        mock.return_value.collection.return_value.document.return_value.set.assert_called()

if __name__ == '__main__':
    unittest.main()
    