import nvme as d
import time

def run_ioworker_test(namespace, block_size, queue_depth):
    """Run an ioworker test with specified parameters."""
    try:
        io_size = block_size // 512  # Convert bytes to 512-byte sectors
        worker = namespace.ioworker(
            io_size=io_size,
            lba_align=io_size,
            lba_random=True,
            qdepth=queue_depth,
            read_percentage=50,  # Mix of read/write
            time=10  # Run for 10 seconds
        )
        result = worker.start().close()
        return {
            "iops": result.io_count_read + result.io_count_nonread,
            "latency_us": result.latency_average * 1000000,  # Convert to microseconds
            "errors": result.error_count if hasattr(result, "error_count") else 0
        }
    except Exception as e:
        print(f"Error running ioworker: {e}")
        return None
