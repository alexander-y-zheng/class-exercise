import logging
import pandas as pd

logger = logging.getLogger(__name__)

def load_netflix(filepath):
    """Load the Netflix CSV file."""
    # Load filepath using pd.read_csv().
    df = pd.read_csv(filepath)

    # Log an INFO.
    logger.info("Data loaded")
    
    # Return the DataFrame.
    return df
