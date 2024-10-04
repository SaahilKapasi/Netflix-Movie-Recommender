"""CSC111 Project 2: Netflix Movie Recommendation System

This file contains functions for loading the graph used for
the Netflix Movie Recommendation System.
"""
import csv
import movie_class


def determine_edge_weight(rating1: int | float, rating2: int | float) -> float:
    """Determines the edge weight to increment the weight between movies by.

    If a user gives a pair of movies the exact same rating, the 'correlation' between the movies is exact,
    and we increment edge weight by 1. If a user rates a movie 5 stars and another movie 0 stars,
    increment the weight by 0.
    """
    return 1 - abs(rating1 - rating2) / 5


def modify_weighted_edge(graph: movie_class.Network, movies_rated: list) -> None:
    """Given a graph and a list of movies rated by a user, adjust the weight of the edges between each
    of the movies, or create a new weighted edge if one is not already present."""
    for i in range(len(movies_rated)):
        for j in range(i + 1, len(movies_rated)):
            movie1, movie2 = movies_rated[i][0], movies_rated[j][0]
            weight = determine_edge_weight(movies_rated[i][1], movies_rated[j][1])

            if weight > 0 and graph.adjacent(movie1, movie2):
                graph.increment_edge(movie1, movie2, weight)
            elif weight > 0:
                graph.add_edge(movie1, movie2, weight)


def load_movie_graph(reviews_file_path: str, movies_file_path: str, movie_limit: int = 1000,
                     rating_limit: int = 1000000) -> movie_class.Network:
    """Returns a movie review weighted graph corresponding to the given datasets.

    Preconditions:
        - reviews_file_path is the path to a CSV file corresponding to the movie review data
        of the format <custID, rating, date, movieID>. The file should also have no header.
        - movies_file_path is the path to a CSV file corresponding to the movie data
        of the format <movieId, releaseYear, title>. The file should have a header.
    """
    graph = movie_class.Network()

    with open(reviews_file_path, 'r') as reviews_file, open(movies_file_path, 'r') as movies_file:
        next(movies_file)
        movies_dict: dict[int, str] = {}
        counter = 0
        for line in csv.reader(movies_file):
            movies_dict[int(line[0])] = line[2]
            graph.add_movie(movies_dict[int(line[0])])
            counter += 1
            if counter == movie_limit:
                break

        user_ratings = {}
        counter = 0
        for line in csv.reader(reviews_file):
            customer, rating, _, movie = line

            if int(movie) in movies_dict:
                if customer not in user_ratings:
                    user_ratings[customer] = []

                user_ratings[customer].append((movies_dict[int(movie)], int(rating)))
                counter += 1

                if counter == rating_limit:
                    break

        for user in user_ratings:
            modify_weighted_edge(graph, user_ratings[user])

    graph.add_sum_of_weights()

    return graph


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv, movie_class'],  # the names (strs) of imported modules
        'allowed-io': ['load_movie_graph'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
