import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    drop_missing_rows,
    remove_duplicates,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # Create a Path object from args.input.
    input_path = Path(args.input)

    # Inside a try block, load that path using pd.read_csv().
    # Catch FileNotFoundError, log an ERROR message,
    # and exit with sys.exit(1).
    # Log an INFO message.
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        logger.error("Input file not found: %s", input_path)
        sys.exit(1)

    logger.info("Loaded %d rows and %d columns", df.shape[0], df.shape[1])
    
    # Call show_overview().
    # Log an INFO message.
    show_overview(df)
    logger.info("Displayed DataFrame overview")

    # Call remove_duplicates().
    original_len = len(df)
    df = remove_duplicates(df)
    logger.info("Removed %d duplicate row(s)", original_len - len(df))

    # Call drop_missing_rows().
    original_len = len(df)
    df = drop_missing_rows(df)
    logger.info("Dropped %d rows with missing values", original_len - len(df))
    
    # Log an INFO message after each step that
    # includes the number of rows removed.

if __name__ == "__main__":
    main()
