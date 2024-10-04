"""CSC111 Project 2: Netflix Movie Recommendation System

This is the graph implementation file of the Netflix Movie Recommendation System.
"""
from __future__ import annotations
from queue import PriorityQueue


class Movie:
    """A vertex in a weighted movie network graph, used to represent a movie.

    Each vertex item is a movie title and is represented by a string.

    Instance Attributes:
        - title: The data stored in this vertex, which is a movie title.
        - neighbours: The vertices that are adjacent to this vertex and
            their corresponding edge weights.
        - community: A value used to group this movie into a group of similar movies.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    title: str
    neighbours: dict[Movie, int | float]
    sum_weights: int | float
    community: str

    def __init__(self, title: str) -> None:
        """Initialize a new movie vertex with the given title, and with
        its community being set to the title to start.

        The vertex is initialized with no neighbours to start.
        """
        self.title = title
        self.neighbours = {}
        self.community = title

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class Network:
    """An implementation of a movie network graph.

    Private Instance Attributes:
        - _movies: A collection of the vertices contained in this graph,
            maps a movie title to a _Movie object.
        - _community: A collection of vertices within a given community
    """
    _movies: dict[str, Movie]
    _communities: dict[str, list[set[Movie] | float]]

    def __init__(self) -> None:
        """Initialize an empty network graph (no vertices or edges)."""
        self._movies = {}
        self._communities = {}

    def add_movie(self, title: str) -> None:
        """Add a movie vertex with the given item to this graph and
        assign it to its own community.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given title is already in this graph.
        """
        if title not in self._movies:
            self._movies[title] = Movie(title)
            self._communities[title] = [{self._movies[title]}, 0.0]

    def add_edge(self, title1: str, title2: str, weight: int | float = 0) -> None:
        """Add an edge with the given weight between the two movies with the given titles.

        Do nothing if there is already an edge between the two movies.

        Raise a ValueError if title1 or title2 do not appear as movies in this graph.

        Preconditions:
            - item1 != item2
        """
        if title1 in self._movies and title2 in self._movies:
            if self._movies[title2] in self.get_neighbours(title1):
                return

            m1 = self._movies[title1]
            m2 = self._movies[title2]

            m1.neighbours[m2] = weight
            m2.neighbours[m1] = weight
        else:
            raise ValueError

    def add_sum_of_weights(self) -> None:
        """This method finds the sum of weights of the neighbours of a movie in order to have a constant step
        access to sum of weights during the modularity calculation"""
        for movie in self._movies:
            self._movies[movie].sum_weights = sum(self._movies[movie].neighbours.values())

    def remove_edge(self, title1: str, title2: str) -> None:
        """Remove an edge between the two movies with the given titles in this graph.

        Raise a ValueError if title1 or title2 do not appear as movies in this graph.

        Preconditions:
            - item1 != item2
            - self._movies[title1] in set(self._movies[title2].neighbours.keys())
        """
        if title1 in self._movies and title2 in self._movies:
            m1 = self._movies[title1]
            m2 = self._movies[title2]

            m1.neighbours.pop(m2)
            m2.neighbours.pop(m1)
        else:
            raise ValueError

    def increment_edge(self, title1: str, title2: str, weight: float) -> None:
        """Increment the edge weight between the two movies with the given titles in this graph.

        Raise a ValueError if title1 or title2 do not appear as movies in this graph.

        Preconditions:
            - item1 != item2
        """
        if title1 in self._movies and title2 in self._movies:
            m1 = self._movies[title1]
            m2 = self._movies[title2]

            m1.neighbours[m2] += weight
            m2.neighbours[m1] += weight
        else:
            raise ValueError

    def get_weight(self, title1: str, title2: str) -> int | float:
        """Return the weight of the edge between the given movies.

        Return 0 if title1 and title2 are not adjacent.

        Raise a ValueError if title1 or title2 do not appear as movies in this graph.
        """
        if title1 in self._movies and title2 in self._movies:
            m1 = self._movies[title1]
            m2 = self._movies[title2]
            return m1.neighbours.get(m2, 0)
        else:
            raise ValueError

    def adjacent(self, title1: str, title2: str) -> bool:
        """Return whether title1 and title2 are adjacent movies in this graph.

        Return False if title1 or title2 do not appear as movies in this graph.
        """
        if title1 in self._movies and title2 in self._movies:
            m1 = self._movies[title1]
            return any(m2.title == title2 for m2 in m1.neighbours)
        else:
            return False

    def get_neighbours(self, title: str) -> set:
        """Return a set of the neighbours of the given movie.

        Note that the *titles* are returned, not the _Movie objects themselves.

        Raise a ValueError if title does not appear as a movie in this graph.
        """
        if title in self._movies:
            m = self._movies[title]
            return {neighbour.title for neighbour in m.neighbours}
        else:
            raise ValueError

    def get_movies(self) -> dict[str, Movie]:
        """A getter method that returns the movies (vertices) found in the graph."""
        return self._movies

    def get_communities(self) -> dict[str, list[set[Movie] | float]]:
        """A getter method that returns the communities found in the graph."""
        return self._communities

    def change_communities(self, vertex: Movie, new_community: str, add_density: float, rem_density: float) -> None:
        """Moves a movie to a new community and update its density"""

        self._communities[vertex.community][0].remove(vertex)
        self._communities[vertex.community][1] -= rem_density
        self._communities[new_community][0].add(vertex)
        self._communities[new_community][1] += add_density

    def remove_empty_communities(self) -> None:
        """Get rid of communities without any members"""
        communities_to_remove = set()

        for community in self._communities:
            if len(self._communities[community][0]) == 0:
                communities_to_remove.add(community)

        for community in communities_to_remove:
            self._communities.pop(community)

    def get_best_movies(self, movies_titles: list[str], limit: int) -> list[str]:
        """Return a maximum length limit of the best _Movie object titles connected to objects in movies
        and in the same community.

        Raise a ValueError if the Movie object is not in this graph
        """
        # PriorityQueue sorts from least to greatest
        pq = PriorityQueue()
        list_of_movies = []
        visited = set()
        movies = [self._movies[title] for title in movies_titles]

        for movie in movies:
            # Should not return itself
            visited.add(movie.title)

            if movie.title not in self._movies:
                # Movie is not in the network
                raise ValueError

            for neighbour in movie.neighbours:
                if neighbour.community == movie.community and neighbour.title not in visited:
                    # Checking if they are in the same community
                    pq.put([-movie.neighbours[neighbour], neighbour.title])
                    # Adding negative weight as priority queue sorts from least to greatest

        for _ in range(limit):
            if pq.empty():
                return list_of_movies

            movie = pq.get()
            # movie[0] = the edge weight (Inversed)
            # movie[1] = the movie object title
            if movie[1] in visited:
                # movie[1] title has already been iterated over
                continue

            list_of_movies.append(movie[1])
            visited.add(movie[1])

            for neighbour in self._movies[movie[1]].neighbours:
                if neighbour.community == self._movies[movie[1]].community and neighbour.title not in visited:
                    # Checking if they are in the same community
                    pq.put([-self._movies[movie[1]].neighbours[neighbour], neighbour.title])
                    # Adding negative weight as priority queue sorts from least to greatest

        return list_of_movies


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['queue'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
