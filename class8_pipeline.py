import logging
from pathlib import Path
from class8_src import load_netflix, require_columns

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    input_path = Path("data/messy_netflix_titles.csv")

    # Inside a try/except block:
    # Load the data and require columns: ["title", "type", "release_year"].
    # Catch ValueError and exit with status code 1.
    try:
        df = load_netflix(input_path)
        df = require_columns(df, ["title", "type", "release_year"])
    except ValueError as e:
        logger.error("Validation error: %s", e)
        exit(1)

    # Log an INFO
    logger.info("Pipeline completed")

    # Log an INFO about the number of rows and columns in the DataFrame.
    logger.info("Data contains %d rows and %d columns.", df.shape[0], df.shape[1])


if __name__ == "__main__":
    main()
