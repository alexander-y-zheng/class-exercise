import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
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

    df_original = df.copy()

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

    # Inside a try block, remove runtime_minutes outliers
    # using remove_iqr_outliers() with a threshold of 1.5.
    # Catch ValueError and exit with sys.exit(1).# Log an INFO message.
    try:
        original_len = len(df)
        df = remove_iqr_outliers(df, "runtime_minutes", 1.5)
        logger.info("Removed %d runtime_minutes outlier(s)", original_len - len(df))
    except ValueError as e:
        logger.error("Error removing runtime_minutes outliers: %s", e)
        sys.exit(1)

    # Apply clean_text() to title, type, and country.
    # Log an INFO message.
    df["title"] = df["title"].apply(clean_text)
    logger.info("Cleaned text column: title")

    df["type"] = df["type"].apply(clean_text)
    logger.info("Cleaned text column: type")

    df["country"] = df["country"].apply(clean_text)
    logger.info("Cleaned text column: country")

    # Create a report (dictionary) containing rows_before, rows_after, rows_removed, and columns.
    rows_before = df_original.shape[0]
    rows_after = df.shape[0]
    rows_removed = rows_before - rows_after
    columns = len(df.columns.tolist())
    report = {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": rows_removed,
        "columns": columns
    }
    # Log an INFO message reporting: rows_before, rows_after, rows_removed, and columns.
    logger.info("Cleaning complete: {'rows_before': %d, 'rows_after': %d, 'rows_removed': %d, 'columns': %d}", 
                report["rows_before"], report["rows_after"], report["rows_removed"], report["columns"])
                
if __name__ == "__main__":
    main()
