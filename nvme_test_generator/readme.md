# NVMe Device Driver Test Script Generator

A Python tool using pynvme to generate test scripts for NVMe driver validation, automating read/write testing with configurable block size and queue depth, and logging results to CSV for analysis.

## Features
- Generates test scripts for NVMe driver validation using pynvme's ioworker.
- Configurable block sizes (e.g., 4KB, 128KB) and queue depths (e.g., 16, 256).
- Logs test results (IOPS, latency, errors) to timestamped CSV files.
- Includes pytest test suite with mocks for reliability.
- Modular design with logging for debugging and extensibility.

## Tech Stack
- Python 3.7+
- pynvme (NVMe testing)
- pytest (testing)
- CSV (result logging)
- Logging (debugging)

## Prerequisites
- Linux (Fedora recommended)
- NVMe SSD (backup data before testing)
- pynvme: Follow installation at https://pynvme.readthedocs.io/en/latest/install.html
- Dependencies: `pip install -r requirements.txt`

## Installation
1. Clone the repo: `git clone https://github.com/14mb1v45h/nvme-test-generator.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up pynvme: `cd /usr/local/pynvme; make setup`
4. Run: `python -m nvme_test_generator.main --pciaddr=01:00.0`

## Usage
- Run with default parameters: `python -m nvme_test_generator.main`
- Customize: `python -m nvme_test_generator.main --block-sizes 4096 131072 --queue-depths 16 256 --output-dir results`
- Results are saved as CSV files in the specified output directory.

## Running Tests
1. Install pytest: `pip install pytest`
2. Run: `pytest nvme_test_generator/tests -v`

## Project Structure
- `main.py`: Entry point with command-line arguments.
- `generator.py`: Core logic for test script generation and execution.
- `utils.py`: Utility functions for running ioworker tests.
- `logging_config.py`: Logging setup.
- `tests/`: Pytest test suite.

## License
MIT License

## GitHub
https://github.com/14mb1v45h/nvme-test-generator
