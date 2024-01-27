import unittest
from unittest.mock import MagicMock

from utils.get_ci_error_statistics import (download_artifact, get_all_errors,
                                           get_artifacts_links,
                                           get_errors_from_single_artifact,
                                           get_job_links, get_model,
                                           make_github_table,
                                           make_github_table_per_model,
                                           reduce_by_error, reduce_by_model)


class TestGetCIErrorStatistics(unittest.TestCase):
    def test_get_job_links(self):
        # Test cases for get_job_links function
        pass

    def test_get_artifacts_links(self):
        # Test cases for get_artifacts_links function
        pass

    def test_download_artifact(self):
        # Test cases for download_artifact function
        pass

    def test_get_errors_from_single_artifact(self):
        # Test cases for get_errors_from_single_artifact function
        pass

    def test_get_all_errors(self):
        # Test cases for get_all_errors function
        pass

    def test_reduce_by_error(self):
        # Test cases for reduce_by_error function
        pass

    def test_get_model(self):
        # Test cases for get_model function
        pass

    def test_reduce_by_model(self):
        # Test cases for reduce_by_model function
        pass

    def test_make_github_table(self):
        # Test cases for make_github_table function
        pass

    def test_make_github_table_per_model(self):
        # Test cases for make_github_table_per_model function
        pass


if __name__ == "__main__":
    unittest.main()
