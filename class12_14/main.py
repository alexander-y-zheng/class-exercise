#main.py

import logging
from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from src import MovieInput, MovieResponse, CSVInfo, DataStorage, ProcessConfig
from middleware import log_requests
from pathlib import Path
import pandas as pd
import io

app = FastAPI(title="Movie API")
storage = DataStorage()
app.middleware("http")(log_requests)


@app.get("/health")
def health_check():
    return {"status": "ok"}

#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}

#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}

@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.

demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}


@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    # 1: return up to limit movies as a list.
    # Log the number returned at INFO.
    # hint: movies is a dictionary whose values are movie records.
    result = list(movies.values())[:limit]
    logger.info("Returned %d movies", len(result))
    return result


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    # 2: 
    # Convert movie to a dictionary, add the new ID, and store it.
    # Log the new ID at INFO and return the stored record.
    final_id = len(movies) + 1
    record = movie.model_dump()
    record["id"] = final_id
    movies[final_id] = record
    logger.info("Added movie: id=%d", final_id)
    return record

@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}


@app.get("/demo/movie-lookup/{movie_id}", response_model=MovieResponse)
def demo_lookup_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        logger.warning(f"Movie not found: {movie_id}")
        raise HTTPException( status_code=404, detail="Movie not found")

    return movie

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    # 2: check the filename extension using pathlib.
    # Reject non-CSV files with status 400 and log a WARNING.
    filename = file.filename
    if filename is None or Path(filename).suffix.lower() != ".csv":
        logger.warning("Non-CSV file uploaded: %s", filename)
        raise HTTPException( status_code=400, detail="Only CSV files are allowed")

    # 3: await the file contents and parse the CSV.
    # Catch expected parsing/decoding errors (e.g. EmptyDataError,ParserError, UnicodeDecodeError) and raise HTTPException
    # with status_code=400.
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
        logger.warning(f"Cannot read CSV: {error}")
        raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")


    # 4: save the DataFrame with storage.save_data().
    # Log the dataset ID, filename at INFO.
    # Return a CSVInfo object with the ID, filename, shape, and column names.
    dataset_id = storage.save_data(df, filename)
    logger.info("Saved dataset: id=%d, filename=%s", dataset_id, filename)
    return CSVInfo(
        filename=filename,
        rows=df.shape[0],
        columns=df.shape[1],
        column_names=list(df.columns),
        dataset_id=dataset_id
    )

@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    # 5: get the DataFrame using storage.get_data().
    # If it is missing, log a WARNING and raise HTTPException with status 404.
    # Otherwise, log successful retrieval at INFO.
    # Return a dictionary with dataset_id, rows, and columns.
    data = storage.get_data(dataset_id)
    if data is None:
        logger.warning("Dataset not found: %d", dataset_id)
        raise HTTPException(status_code=404, detail="Dataset not found")
    logger.info("Retrieved dataset: id=%d", dataset_id)
    return {
        "dataset_id": dataset_id,
        "rows": data.shape[0],
        "columns": data.shape[1]
    }
    
@app.post("/demo/process-config")
def demo_process_config(config: ProcessConfig):
    df = pd.DataFrame({"title": ["Movie A", "Movie A", "Movie B", None]})
    settings = config.model_dump()

    if settings["processing"]["remove_duplicates"]:
        df = df.drop_duplicates()

    if settings["processing"]["drop_missing"]:
        df = df.dropna()
        
    return {"rows": len(df)}

