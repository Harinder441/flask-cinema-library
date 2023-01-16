import requests as req

API_ENDPOINT = "https://api.themoviedb.org/3"
API_KEY = YOUR-API-KEY
QUERY_ENDPOINT = API_ENDPOINT + "/search/movie"

#give list of movies that matches the title in query
def get_movie_list(query: str):
    parameters = {
        "api_key": API_KEY,
        "query": query,
    }
    header = {
        'Content-Type': 'application/json;charset=utf-8',
    }
    res = req.get(url=QUERY_ENDPOINT, params=parameters, headers=header)
    res.raise_for_status()
    return res.json()['results']

#give movies detail by id
def get_movie(id_: int):
    movie_endpoint = API_ENDPOINT + f"/movie/{id_}"
    parameters = {
        "api_key": API_KEY,
    }
    header = {
        'Content-Type': 'application/json;charset=utf-8',
    }
    res = req.get(url=movie_endpoint, params=parameters, headers=header)
    res.raise_for_status()
    return res.json()
