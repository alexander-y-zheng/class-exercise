import logging

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    # Log a DEBUG message containing the shape.
    logger.debug("DataFrame shape: %s rows, %s columns", df.shape[0], df.shape[1])

    # Print the shape, first five rows, column names, and data types.
    print("Shape:", df.shape)
    print("First five rows:\n", df.head(5))
    print("Column names:", df.columns.tolist())
    print("Data types:\n", df.dtypes)


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    # Remove exact duplicate rows.
    before_rows = df.shape[0]
    df = df.drop_duplicates()
    after_rows = df.shape[0]

    # Log a DEBUG message containing the before and after row counts.
    logger.debug("Removed duplicates: %s rows before, %s rows after", before_rows, after_rows)
    
    # Return the resulting DataFrame.
    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    # Drop rows containing one or more missing values.
    before_rows = df.shape[0]
    df = df.dropna()
    after_rows = df.shape[0]

    # Log a DEBUG message containing the before and after row counts.
    logger.debug("Dropped missing rows: %s rows before, %s rows after", before_rows, after_rows)
    
    # Return the resulting DataFrame.
    return df
