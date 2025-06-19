import argparse
from nvme_test_generator.generator import NVMeTestGenerator
from nvme_test_generator.logging_config import setup_logging

def main():
    logger = setup_logging()
    parser = argparse.ArgumentParser(description="NVMe Device Driver Test Script Generator")
    parser.add_argument("--pciaddr", default="01:00.0", help="PCI address of NVMe device (e.g., 01:00.0)")
    parser.add_argument("--block-sizes", nargs="+", type=int, default=[4096, 131072], help="Block sizes in bytes")
    parser.add_argument("--queue-depths", nargs="+", type=int, default=[16, 256], help="Queue depths")
    parser.add_argument("--output-dir", default="test_results", help="Output directory for CSV results")
    args = parser.parse_args()

    logger.info("Starting NVMe Test Script Generator")
    generator = NVMeTestGenerator(
        pci_addr=args.pciaddr,
        block_sizes=args.block_sizes,
        queue_depths=args.queue_depths,
        output_dir=args.output_dir
    )
    generator.generate_and_run_tests()

if __name__ == "__main__":
    main()