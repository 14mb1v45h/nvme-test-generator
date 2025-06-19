import pytest
import os
from unittest.mock import patch, MagicMock
from nvme_test_generator.generator import NVMeTestGenerator

@pytest.fixture
def generator(tmp_path):
    output_dir = tmp_path / "test_results"
    return NVMeTestGenerator(
        pci_addr="01:00.0",
        block_sizes=[4096],
        queue_depths=[16],
        output_dir=str(output_dir)
    )

class TestNVMeTestGenerator:
    @patch("nvme_test_generator.generator.d.Pcie")
    @patch("nvme_test_generator.generator.run_ioworker_test")
    def test_generate_and_run_tests(self, mock_ioworker, mock_pcie, generator):
        mock_pcie.return_value = MagicMock()
        controller = MagicMock()
        namespace = MagicMock()
        mock_pcie.return_value.Controller.return_value = controller
        controller.Namespace.return_value = namespace
        mock_ioworker.return_value = {
            "iops": 10000,
            "latency_us": 200,
            "errors": 0
        }

        generator.generate_and_run_tests()
        assert mock_ioworker.called
        csv_files = [f for f in os.listdir(generator.output_dir) if f.endswith(".csv")]
        assert len(csv_files) == 1

    def test_log_results_to_csv(self, generator, tmp_path):
        results = [{
            "timestamp": "2025-06-19 12:00:00",
            "block_size": 4096,
            "queue_depth": 16,
            "iops": 10000,
            "latency_us": 200,
            "errors": 0
        }]
        generator.log_results_to_csv(results)
        csv_files = [f for f in os.listdir(generator.output_dir) if f.endswith(".csv")]
        assert len(csv_files) == 1
        with open(os.path.join(generator.output_dir, csv_files[0]), "r") as f:
            content = f.read()
            assert "10000" in content
            assert "200" in content