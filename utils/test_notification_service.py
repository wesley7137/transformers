import unittest
from unittest.mock import MagicMock, patch

from utils.notification_service import Message, WebClient


class TestNotificationService(unittest.TestCase):
    def setUp(self):
        self.message = Message("title", "ci_title", {}, {})

    @patch.object(WebClient, 'chat_postMessage')
    def test_error_out_valid_token(self, mock_chat_postMessage):
        mock_chat_postMessage.return_value = MagicMock(ok=True)
        self.message.error_out("title", "ci_title")
        mock_chat_postMessage.assert_called_once()

    @patch.object(WebClient, 'chat_postMessage')
    def test_error_out_invalid_token(self, mock_chat_postMessage):
        mock_chat_postMessage.return_value = MagicMock(ok=False, error='not_authed')
        with self.assertRaises(Exception):
            self.message.error_out("title", "ci_title")
        mock_chat_postMessage.assert_called_once()

if __name__ == '__main__':
    unittest.main()
