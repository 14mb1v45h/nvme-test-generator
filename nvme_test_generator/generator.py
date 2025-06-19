import os
import nvme as d
import csv
from datetime import datetime
from .utils import run_ioworker_test
from .logging_config import setup_logging

class NVMeTestGenerator:
    def __init__(self, pci_addr, block_sizes, queue_depths, output_dir):
        self.pci_addr = pci_addr
        self.block_sizes = block_sizes
        self.queue_depths = queue_depths
        self.output_dir = output_dir
        self.logger = setup_logging()
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_and_run_tests(self):
        """Generate and run NVMe test scripts for all parameter combinations."""
        self.logger.info(f"Initializing NVMe controller at {self.pci_addr}")
        try:
            pcie = d.Pcie(self.pci_addr)
            controller = d.Controller(pcie)
            namespace = d.Namespace(controller, 1)
        except Exception as e:
            self.logger.error(f"Failed to initialize NVMe device: {e}")
            raise

        results = []
        for bs in self.block_sizes:
            for qd in self.queue_depths:
                self.logger.info(f"Running test: block_size={bs}, queue_depth={qd}")
                result = run_ioworker_test(namespace, bs, qd)
                if result:
                    results.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "block_size": bs,
                        "queue_depth": qd,
                        "iops": result.get("iops", 0),
                        "latency_us": result.get("latency_us", 0),
                        "errors": result.get("errors", 0)
                    })
                else:
                    self.logger.error(f"Test failed: block_size={bs}, queue_depth={qd}")

        self.log_results_to_csv(results)
        namespace.close()
        controller.reset()

    def log_results_to_csv(self, results):
        """Log test results to a CSV file."""
        if not results:
            self.logger.warning("No results to log")
            return

        csv_path = os.path.join(self.output_dir, f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        self.logger.info(f"Logging results to {csv_path}")
        try:
            with open(csv_path, mode="w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["timestamp", "block_size", "queue_depth", "iops", "latency_us", "errors"])
                writer.writeheader()
                for result in results:
                    writer.writerow(result)
        except Exception as e:
            self.logger.error(f"Failed to write CSV: {e}")