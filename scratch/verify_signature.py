import logging
import os
import sys
from runner.config import RunnerConfig
from runner.core import run_one

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("VERIFY")

# Get absolute path to mock html
mock_path = os.path.abspath("scratch/mock_signature.html")
mock_url = f"file:///{mock_path.replace('\\', '/')}"

cfg = RunnerConfig(
    start_url=mock_url,
    headless=True,
    max_steps_per_response=2,
    out_dir="scratch/logs"
)

logger.info(f"Starting verification on: {mock_url}")

success = run_one(cfg, logger, 1)

if success:
    logger.info("Verification PASSED: Runner successfully signed and moved past the mock page.")
    sys.exit(0)
else:
    logger.error("Verification FAILED: Runner could not move past the mock page.")
    sys.exit(1)
