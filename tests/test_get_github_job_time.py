import unittest
from unittest import mock

from utils.get_github_job_time import (extract_time_from_single_job,
                                       get_job_time)


class TestGetGithubJobTime(unittest.TestCase):
    @mock.patch("utils.get_github_job_time.requests")
    def test_extract_time_from_single_job(self, mock_requests):
        # Mock the necessary API response
        job = {
            "name": "Job 1",
            "started_at": "2022-01-01T00:00:00Z",
            "completed_at": "2022-01-01T01:00:00Z",
        }

        # Call the function being tested
        job_info = extract_time_from_single_job(job)

        # Assert the extracted job info
        self.assertEqual(job_info["started_at"], "2022-01-01T00:00:00Z")
        self.assertEqual(job_info["completed_at"], "2022-01-01T01:00:00Z")
        self.assertEqual(job_info["duration"], 60)

    @mock.patch("utils.get_github_job_time.requests")
    def test_get_job_time(self, mock_requests):
        # Mock the necessary API response
        workflow_run_id = "123456789"
        mock_requests.get.return_value.json.return_value = {
            "jobs": [
                {
                    "name": "Job 1",
                    "started_at": "2022-01-01T00:00:00Z",
                    "completed_at": "2022-01-01T01:00:00Z",
                },
                {
                    "name": "Job 2",
                    "started_at": "2022-01-01T02:00:00Z",
                    "completed_at": "2022-01-01T03:00:00Z",
                },
            ],
            "total_count": 2,
        }

        # Call the function being tested
        job_time = get_job_time(workflow_run_id)

        # Assert the extracted job times
        self.assertEqual(len(job_time), 2)
        self.assertEqual(job_time["Job 1"]["duration"], 60)
        self.assertEqual(job_time["Job 2"]["duration"], 60)


if __name__ == "__main__":
    unittest.main()
