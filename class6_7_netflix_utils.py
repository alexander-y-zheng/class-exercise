import logging
import re
import pandas as pd

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

def clean_text(value):
    """Normalize one text value."""
    # Strip surrounding whitespace.
    value = value.strip()

    # Convert text to lowercase.
    value = value.lower()

    # Collapse repeated whitespace.
    value = re.sub(r'\s+', ' ', value)
    
    return value


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # If column does not exist:
    if column not in df.columns:
        logger.error("Column not found: %s", column)
        raise ValueError(f"Column not found: {column}")

    # Calculate Q1, Q3, and IQR.
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Use threshold to calculate lower and upper bounds.
    lower = Q1 - threshold * IQR
    upper = Q3 + threshold * IQR

    # Keep rows inside the bounds.
    before_rows = df.shape[0]
    df = df[(df[column] >= lower) & (df[column] <= upper)]
    after_rows = df.shape[0]

    # Log a DEBUG message containing the bounds and the number of rows removed.
    logger.debug("Removed IQR outliers from column '%s': lower=%s, upper=%s, rows removed=%s",
                 column, lower, upper, before_rows - after_rows)

    # Return the resulting DataFrame.
    return df
