import unittest
from unittest.mock import MagicMock, patch

from utils.get_ci_error_statistics import (download_artifact, get_all_errors,
                                           get_artifacts_links,
                                           get_errors_from_single_artifact,
                                           get_job_links, make_github_table,
                                           make_github_table_per_model,
                                           reduce_by_error, reduce_by_model)


class TestGetCIErrorStatistics(unittest.TestCase):
    @patch("utils.get_ci_error_statistics.requests.get")
    def test_get_job_links(self, mock_get):
        # Test case for valid workflow run ID and token
        workflow_run_id = "12345"
        token = "abc123"
        mock_get.return_value.json.return_value = {
            "jobs": [
                {"name": "job1", "html_url": "https://github.com/job1"},
                {"name": "job2", "html_url": "https://github.com/job2"},
            ]
        }
        job_links = get_job_links(workflow_run_id, token)
        self.assertEqual(job_links, {"job1": "https://github.com/job1", "job2": "https://github.com/job2"})

        # Test case for invalid workflow run ID
        workflow_run_id = "invalid"
        job_links = get_job_links(workflow_run_id, token)
        self.assertEqual(job_links, {})

        # Test case for missing token
        workflow_run_id = "12345"
        token = None
        job_links = get_job_links(workflow_run_id, token)
        self.assertEqual(job_links, {})

    @patch("utils.get_ci_error_statistics.requests.get")
    def test_get_artifacts_links(self, mock_get):
        # Test case for valid workflow run ID and token
        workflow_run_id = "12345"
        token = "abc123"
        mock_get.return_value.json.return_value = {
            "artifacts": [
                {"name": "artifact1", "archive_download_url": "https://github.com/artifact1"},
                {"name": "artifact2", "archive_download_url": "https://github.com/artifact2"},
            ]
        }
        artifacts = get_artifacts_links(workflow_run_id, token)
        self.assertEqual(
            artifacts,
            {"artifact1": "https://github.com/artifact1", "artifact2": "https://github.com/artifact2"},
        )

        # Test case for invalid workflow run ID
        workflow_run_id = "invalid"
        artifacts = get_artifacts_links(workflow_run_id, token)
        self.assertEqual(artifacts, {})

        # Test case for missing token
        workflow_run_id = "12345"
        token = None
        artifacts = get_artifacts_links(workflow_run_id, token)
        self.assertEqual(artifacts, {})

    @patch("utils.get_ci_error_statistics.requests.get")
    @patch("utils.get_ci_error_statistics.requests.exceptions.RequestException")
    def test_download_artifact(self, mock_request_exception, mock_get):
        # Test case for valid artifact URL, output directory, and token
        artifact_name = "artifact1"
        artifact_url = "https://github.com/artifact1"
        output_dir = "/path/to/output"
        token = "abc123"
        mock_get.return_value.headers = {"Location": "https://github.com/download"}
        mock_get.return_value.content = b"artifact content"
        with patch("builtins.open", MagicMock()) as mock_open:
            download_artifact(artifact_name, artifact_url, output_dir, token)
            mock_open.assert_called_once_with("/path/to/output/artifact1.zip", "wb")
            mock_open.return_value.__enter__.return_value.write.assert_called_once_with(b"artifact content")

        # Test case for invalid artifact URL
        artifact_name = "artifact1"
        artifact_url = "invalid"
        output_dir = "/path/to/output"
        token = "abc123"
        with patch("builtins.open", MagicMock()) as mock_open:
            download_artifact(artifact_name, artifact_url, output_dir, token)
            mock_open.assert_not_called()

        # Test case for missing token
        artifact_name = "artifact1"
        artifact_url = "https://github.com/artifact1"
        output_dir = "/path/to/output"
        token = None
        with patch("builtins.open", MagicMock()) as mock_open:
            download_artifact(artifact_name, artifact_url, output_dir, token)
            mock_open.assert_not_called()

    def test_get_errors_from_single_artifact(self):
        # TODO: Write test cases for get_errors_from_single_artifact function
        pass

    def test_get_all_errors(self):
        # TODO: Write test cases for get_all_errors function
        pass

    def test_reduce_by_error(self):
        # TODO: Write test cases for reduce_by_error function
        pass

    def test_reduce_by_model(self):
        # TODO: Write test cases for reduce_by_model function
        pass

    def test_make_github_table(self):
        # TODO: Write test cases for make_github_table function
        pass

    def test_make_github_table_per_model(self):
        # TODO: Write test cases for make_github_table_per_model function
        pass

if __name__ == "__main__":
    unittest.main()
