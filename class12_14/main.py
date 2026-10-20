#main.py

import logging
from fastapi import FastAPI, Query
from src import MovieInput, MovieResponse

app = FastAPI(title="Movie API")


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