import pytest
from unittest.mock import patch, MagicMock
from nvme_test_generator.utils import run_ioworker_test

class TestUtils:
    @patch("nvme_test_generator.utils.d.Namespace.ioworker")
    def test_run_ioworker_test_success(self, mock_ioworker):
        namespace = MagicMock()
        worker = MagicMock()
        result = MagicMock()
        result.io_count_read = 5000
        result.io_count_nonread = 5000
        result.latency_average = 0.0002  # 200 microseconds
        result.error_count = 0
        worker.start.return_value.close.return_value = result
        mock_ioworker.return_value = worker

        test_result = run_ioworker_test(namespace, block_size=4096, queue_depth=16)
        assert test_result == {
            "iops": 10000,
            "latency_us": 200,
            "errors": 0
        }

    @patch("nvme_test_generator.utils.d.Namespace.ioworker")
    def test_run_ioworker_test_failure(self, mock_ioworker):
        namespace = MagicMock()
        mock_ioworker.side_effect = Exception("IO error")
        test_result = run_ioworker_test(namespace, block_size=4096, queue_depth=16)
        assert test_result is None