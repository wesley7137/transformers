import unittest
from unittest.mock import MagicMock, patch

from utils.notification_service_doc_tests import \
    retrieve_available_artifacts  # Other functions to import


class TestNotificationServiceDocTests(unittest.TestCase):
    @patch("utils.notification_service_doc_tests.os.listdir")
    def test_retrieve_available_artifacts(self, mock_listdir):
        # Test case for valid directories and artifact paths
        mock_listdir.return_value = ["artifact1", "artifact2"]
        artifacts = retrieve_available_artifacts()
        self.assertEqual(artifacts, {"artifact1": [], "artifact2": []})

        # Test case for empty directories
        mock_listdir.return_value = []
        artifacts = retrieve_available_artifacts()
        self.assertEqual(artifacts, {})

        # Test case for directories with subdirectories
        mock_listdir.return_value = ["artifact1", "subdir"]
        artifacts = retrieve_available_artifacts()
        self.assertEqual(artifacts, {"artifact1": []})

        # TODO: Write more test cases for other functions

if __name__ == "__main__":
    unittest.main()
