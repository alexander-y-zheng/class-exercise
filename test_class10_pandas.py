#test_class10_pandas.py
import pandas as pd
import pytest

def test_dataframe_shape(sample_df):
    # This DataFrame has 5 rows and 4 columns.
    df = sample_df

    # assert checks a condition. If it is true, the test continues. If it is false, the test fails.
    assert sample_df.shape == (5, 4)
    # assert df.shape == (1, 1) 
    # ^ will get an AssertionError

def test_drop_duplicates(sample_df):
    # Arrange
    df = sample_df
    # note: the final two rows are identical, so removing duplicates leaves four rows and four columns.

    # Act
    result = sample_df.drop_duplicates()

    # Assert
    assert result.shape == (4, 4)
    assert result["title"].tolist() == ["Movie A", "Movie B", "Movie C", "Movie D"]

def test_invalid_numeric_value():
    df = pd.DataFrame({"rating": [7, "unknown", 9]})

    with pytest.raises(ValueError):
        pd.to_numeric(df["rating"])

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })