import json
import os
import unittest
from unittest.mock import patch

from utils.get_ci_error_statistics import (download_artifact, get_all_errors,
                                           get_artifacts_links,
                                           get_errors_from_single_artifact,
                                           get_job_links, make_github_table,
                                           make_github_table_per_model,
                                           reduce_by_error, reduce_by_model)


class TestGetCIErrorStatistics(unittest.TestCase):
    @patch("utils.get_ci_error_statistics.requests.get")
    def test_get_job_links_success(self, mock_get):
        # Mock the response from the GitHub API
        mock_get.return_value.json.return_value = {
            "jobs": [
                {"name": "job1", "html_url": "https://github.com/job1"},
                {"name": "job2", "html_url": "https://github.com/job2"},
            ]
        }

        workflow_run_id = "12345"
        token = "TOKEN"

        job_links = get_job_links(workflow_run_id, token=token)

        self.assertEqual(len(job_links), 2)
        self.assertEqual(job_links["job1"], "https://github.com/job1")
        self.assertEqual(job_links["job2"], "https://github.com/job2")

    @patch("utils.get_ci_error_statistics.requests.get")
    def test_get_job_links_failure(self, mock_get):
        # Mock an exception when making the API request
        mock_get.side_effect = Exception("API request failed")

        workflow_run_id = "12345"
        token = "TOKEN"

        job_links = get_job_links(workflow_run_id, token=token)

        self.assertEqual(len(job_links), 0)

    @patch("utils.get_ci_error_statistics.requests.get")
    def test_get_artifacts_links_success(self, mock_get):
        # Mock the response from the GitHub API
        mock_get.return_value.json.return_value = {
            "artifacts": [
                {"name": "artifact1", "archive_download_url": "https://github.com/artifact1"},
                {"name": "artifact2", "archive_download_url": "https://github.com/artifact2"},
            ]
        }

        workflow_run_id = "12345"
        token = "TOKEN"

        artifacts = get_artifacts_links(workflow_run_id, token=token)

        self.assertEqual(len(artifacts), 2)
        self.assertEqual(artifacts["artifact1"], "https://github.com/artifact1")
        self.assertEqual(artifacts["artifact2"], "https://github.com/artifact2")

    @patch("utils.get_ci_error_statistics.requests.get")
    def test_get_artifacts_links_failure(self, mock_get):
        # Mock an exception when making the API request
        mock_get.side_effect = Exception("API request failed")

        workflow_run_id = "12345"
        token = "TOKEN"

        artifacts = get_artifacts_links(workflow_run_id, token=token)

        self.assertEqual(len(artifacts), 0)

    @patch("utils.get_ci_error_statistics.requests.get")
    def test_download_artifact_success(self, mock_get):
        # Mock the response from the GitHub API
        mock_get.return_value.headers = {"Location": "https://github.com/artifact1"}
        mock_get.return_value.content = b"Artifact content"

        artifact_name = "artifact1"
        artifact_url = "https://github.com/artifact1"
        output_dir = "output"
        token = "TOKEN"

        with patch("builtins.open", create=True) as mock_open:
            download_artifact(artifact_name, artifact_url, output_dir, token)

            mock_open.assert_called_once_with(os.path.join(output_dir, f"{artifact_name}.zip"), "wb")
            mock_open.return_value.__enter__.return_value.write.assert_called_once_with(b"Artifact content")

    @patch("utils.get_ci_error_statistics.requests.get")
    def test_download_artifact_failure(self, mock_get):
        # Mock an exception when making the API request
        mock_get.side_effect = Exception("API request failed")

        artifact_name = "artifact1"
        artifact_url = "https://github.com/artifact1"
        output_dir = "output"
        token = "TOKEN"

        with patch("builtins.open", create=True) as mock_open:
            download_artifact(artifact_name, artifact_url, output_dir, token)

            mock_open.assert_not_called()

    def test_get_errors_from_single_artifact(self):
        artifact_zip_path = "artifact.zip"
        job_links = {"job1": "https://github.com/job1"}

        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = "error1: Failed test1\nerror2: Failed test2"

            errors = get_errors_from_single_artifact(artifact_zip_path, job_links=job_links)

            self.assertEqual(len(errors), 2)
            self.assertEqual(errors[0], ["error1", "Failed test1", "job1"])
            self.assertEqual(errors[1], ["error2", "Failed test2", "job1"])

    def test_get_all_errors(self):
        artifact_dir = "artifacts"
        job_links = {"job1": "https://github.com/job1"}

        with patch("os.listdir") as mock_listdir:
            mock_listdir.return_value = ["artifact1.zip", "artifact2.zip"]

            with patch("utils.get_ci_error_statistics.get_errors_from_single_artifact") as mock_get_errors:
                mock_get_errors.side_effect = [
                    [["error1", "Failed test1", "job1"]],
                    [["error2", "Failed test2", "job1"]],
                ]

                errors = get_all_errors(artifact_dir, job_links=job_links)

                self.assertEqual(len(errors), 2)
                self.assertEqual(errors[0], ["error1", "Failed test1", "job1"])
                self.assertEqual(errors[1], ["error2", "Failed test2", "job1"])

    def test_reduce_by_error(self):
        logs = [
            ["error1", "Failed test1", "job1"],
            ["error1", "Failed test2", "job1"],
            ["error2", "Failed test3", "job1"],
        ]
        error_filter = ["error1"]

        reduced_by_error = reduce_by_error(logs, error_filter=error_filter)

        self.assertEqual(len(reduced_by_error), 1)
        self.assertEqual(reduced_by_error["error2"]["count"], 1)
        self.assertEqual(reduced_by_error["error2"]["failed_tests"], [("Failed test3", "job1")])

    def test_reduce_by_model(self):
        logs = [
            ["error1", "Failed test1", "model1"],
            ["error1", "Failed test2", "model1"],
            ["error2", "Failed test3", "model2"],
        ]
        error_filter = ["error1"]

        reduced_by_model = reduce_by_model(logs, error_filter=error_filter)

        self.assertEqual(len(reduced_by_model), 2)
        self.assertEqual(reduced_by_model["model1"]["count"], 2)
        self.assertEqual(reduced_by_model["model1"]["errors"], {"error1": 2})
        self.assertEqual(reduced_by_model["model2"]["count"], 1)
        self.assertEqual(reduced_by_model["model2"]["errors"], {"error2": 1})

    def test_make_github_table(self):
        reduced_by_error = {
            "error1": {"count": 2, "failed_tests": [("Failed test1", "job1"), ("Failed test2", "job1")]},
            "error2": {"count": 1, "failed_tests": [("Failed test3", "job1")]},
        }

        table = make_github_table(reduced_by_error)

        expected_table = "| no. | error | status |\n|-:|:-|:-|\n| 2 | error1 |  |\n| 1 | error2 |  |\n"

        self.assertEqual(table, expected_table)

    def test_make_github_table_per_model(self):
        reduced_by_model = {
            "model1": {"count": 2, "errors": {"error1": 2}},
            "model2": {"count": 1, "errors": {"error2": 1}},
        }

        table = make_github_table_per_model(reduced_by_model)

        expected_table = "| model | no. of errors | major error | count |\n|-:|-:|-:|-:|\n| model1 | 2 | error1 | 2 |\n| model2 | 1 | error2 | 1 |\n"

        self.assertEqual(table, expected_table)


if __name__ == "__main__":
    unittest.main()
