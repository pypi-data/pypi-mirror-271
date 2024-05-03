import json
import unittest
from unittest.mock import patch, mock_open
import urllib3

from aihub.api.run_api import RunApi


class TestRunApi(unittest.TestCase):
    """RunApi unit test stubs"""

    def setUp(self) -> None:
        self.api = RunApi()

    def tearDown(self) -> None:
        pass

    @patch.object(urllib3.PoolManager, 'request')
    def test_get_run_results(self, mock_request) -> None:
        """Test case for get_run_results

        Retrieve run results
        """
        run_id = "run123"
        expected_response = {
            "files": [
                {"original_file_name": "data.pdf", "documents": []}
            ],
            "has_more": False
        }

        mock_response = urllib3.HTTPResponse(body=bytes(json.dumps(expected_response), 'utf-8'), status=200)
        mock_request.return_value = mock_response

        response = self.api.get_run_results(run_id)
        self.assertFalse(response.has_more)
        self.assertEqual(len(response.files), 1)
        self.assertEqual(response.files[0].original_file_name, "data.pdf")

    @patch.object(urllib3.PoolManager, 'request')
    def test_get_run_status(self, mock_request) -> None:
        """Test case for get_run_status

        Get the status of a run.
        """
        run_id = "run123"
        expected_response = {"id": run_id, "status": "COMPLETE"}

        mock_response = urllib3.HTTPResponse(body=bytes(json.dumps(expected_response), 'utf-8'), status=200)
        mock_request.return_value = mock_response

        response = self.api.get_run_status(run_id)
        self.assertEqual(response.id, run_id)
        self.assertEqual(response.status, "COMPLETE")

    @patch.object(urllib3.PoolManager, 'request')
    def test_run_app(self, mock_request) -> None:
        """Test case for run_app

        Run a given app.
        """
        app_id = "app123"
        batch_id = 123
        expected_response = {"id": "run123", "status": "RUNNING"}

        mock_response = urllib3.HTTPResponse(body=bytes(json.dumps(expected_response), 'utf-8'), status=200)
        mock_request.return_value = mock_response

        response = self.api.run_app({ 'app_id': app_id, 'batch_id': batch_id})
        self.assertEqual(response.id, "run123")
        self.assertEqual(response.status, "RUNNING")

    @patch('builtins.open', new_callable=mock_open, read_data='DUMMY FILE CONTENT')
    @patch.object(urllib3.PoolManager, 'request')
    def test_run_app_sync(self, mock_request, mock_file_open) -> None:
        """Test case for run_app_sync

        Run a given app and return the results.
        """
        app_name = "test_app_sync"
        files = ["data1.pdf"]
        expected_response = {
            "files": [
                {"original_file_name": "data1.pdf", "documents": []}
            ],
            "has_more": False
        }

        mock_response = urllib3.HTTPResponse(body=bytes(json.dumps(expected_response), 'utf-8'), status=200)
        mock_request.return_value = mock_response

        # Assuming the `run_app_sync` method accepts a list of file paths
        # and internally handles file reading or other preprocessing
        response = self.api.run_app_sync(app_name=app_name, files=files)
        self.assertFalse(response.has_more)
        self.assertEqual(len(response.files), 1)
        self.assertEqual(response.files[0].original_file_name, "data1.pdf")



if __name__ == '__main__':
    unittest.main()
