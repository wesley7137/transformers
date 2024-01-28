import unittest
from unittest import mock

from utils.extract_warnings import (extract_warnings,
                                    extract_warnings_from_single_artifact)


class TestExtractWarnings(unittest.TestCase):
    @mock.patch("utils.extract_warnings.os")
    @mock.patch("utils.extract_warnings.zipfile")
    def test_extract_warnings_from_single_artifact_valid(self, mock_zipfile, mock_os):
        # Mock the necessary dependencies and API requests
        mock_zipfile.ZipFile.return_value.__enter__.return_value.namelist.return_value = ["warnings.txt"]
        mock_os.path.isdir.return_value = False

        # Create a valid artifact file path
        artifact_path = "valid_artifact.zip"

        # Define the expected warnings
        expected_warnings = {"Warning 1", "Warning 2"}

        # Call the function being tested
        warnings = extract_warnings_from_single_artifact(artifact_path, ["Warning"])

        # Assert that the extracted warnings match the expected warnings
        self.assertEqual(warnings, expected_warnings)

    @mock.patch("utils.extract_warnings.os")
    @mock.patch("utils.extract_warnings.zipfile")
    def test_extract_warnings_from_single_artifact_invalid(self, mock_zipfile, mock_os):
        # Mock the necessary dependencies and API requests
        mock_zipfile.ZipFile.side_effect = Exception("Invalid zip file")

        # Create an invalid artifact file path
        artifact_path = "invalid_artifact.zip"

        # Call the function being tested
        warnings = extract_warnings_from_single_artifact(artifact_path, ["Warning"])

        # Assert that no warnings are extracted
        self.assertEqual(warnings, set())

    @mock.patch("utils.extract_warnings.os")
    @mock.patch("utils.extract_warnings.zipfile")
    def test_extract_warnings_valid(self, mock_zipfile, mock_os):
        # Mock the necessary dependencies and API requests
        mock_os.listdir.return_value = ["valid_artifact.zip"]
        mock_os.path.isdir.return_value = False
        mock_zipfile.ZipFile.return_value.__enter__.return_value.namelist.return_value = ["warnings.txt"]

        # Create a valid artifact directory
        artifact_dir = "valid_artifact_dir"

        # Define the expected warnings
        expected_warnings = {"Warning 1", "Warning 2"}

        # Call the function being tested
        warnings = extract_warnings(artifact_dir, ["Warning"])

        # Assert that the extracted warnings match the expected warnings
        self.assertEqual(warnings, expected_warnings)

    @mock.patch("utils.extract_warnings.os")
    @mock.patch("utils.extract_warnings.zipfile")
    def test_extract_warnings_invalid(self, mock_zipfile, mock_os):
        # Mock the necessary dependencies and API requests
        mock_os.listdir.return_value = ["invalid_artifact.zip"]
        mock_os.path.isdir.return_value = False
        mock_zipfile.ZipFile.side_effect = Exception("Invalid zip file")

        # Create an invalid artifact directory
        artifact_dir = "invalid_artifact_dir"

        # Call the function being tested
        warnings = extract_warnings(artifact_dir, ["Warning"])

        # Assert that no warnings are extracted
        self.assertEqual(warnings, set())


if __name__ == "__main__":
    unittest.main()
