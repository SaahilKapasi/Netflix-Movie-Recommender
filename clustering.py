"""CSC111 Project 2: Netflix Movie Recommendation System

This is the file for implementing the clustering functionality
of the Netflix Movie Recommendation System.
"""
import movie_class


def sigma_in(community: list[set[movie_class.Movie] | float]) -> float:
    """A helper function to find the sum of all the weighted edges strictly inside community."""
    return community[1]


def sigma_total(community: list[set[movie_class.Movie] | float]) -> float:
    """A helper function to find the sum of all the edges inside the community.
    The sum of all incident edges double counts edges in the community, so subtract them to get sum of all weighted
    incident edges."""
    incident_edges = 0
    for vertex in community[0]:
        incident_edges += vertex.sum_weights
    return incident_edges - sigma_in(community)


def k_i_in(added_vertex: movie_class.Movie, community: list[set[movie_class.Movie] | float]) -> float:
    """A helper function to calculate the sum of all the weighted edges that added_vertex connect to
    inside the new community we are considering merging it into."""
    incident_edges = 0

    for community_vertex in community[0]:
        if added_vertex in community_vertex.neighbours:
            incident_edges += added_vertex.neighbours[community_vertex]

    return incident_edges


def k_i_out(removed_vertex: movie_class.Movie, community: list[set[movie_class]]) -> float:
    """Helper function to calculate the sum of all the weighted edges that removed_vertex connect to in
    its original community."""
    removed_edges = 0
    for vertex in community[0]:
        if vertex in removed_vertex.neighbours:
            removed_edges += removed_vertex.neighbours[vertex]
    return removed_edges


def k_i(added_vertex: movie_class.Movie) -> float:
    """Helper function to return the sum of weighted of the edges of a given vertex."""
    return added_vertex.sum_weights


def m_func(graph: movie_class.Network) -> float:
    """A function to determine the sum of weighted edges of an entire graph."""
    all_edge_weight = 0
    for vertex in graph.get_movies():
        all_edge_weight += graph.get_movies()[vertex].sum_weights
    return all_edge_weight / 2


def calculate_delta_q(community: list[set[movie_class.Movie] | float], vertex: movie_class.Movie, m: float) -> float:
    """Used to calculate delta_q, this is an implementation of the formula given in the paper to
    efficiently calculate the change in modularity"""
    sum_in = sigma_in(community)
    sum_total = sigma_total(community)
    ki = k_i(vertex)
    kin = k_i_in(vertex, community)
    return (((sum_in + kin) / (2 * m)) - (((sum_total + ki) / (2 * m)) ** 2)
            ) - ((sum_in / (2 * m)) - ((sum_total / (2 * m)) ** 2) - (ki / (2 * m)) ** 2)


def louvain_helper(graph: movie_class.Network, vertex: movie_class.Movie, m: float) -> None:
    """Helper function to help simplify the Louvain's method.
    For a given vertex, iterate over its neighbours and check the modularity gain from assigning
    a vertex to its neighbors community. If the size of the community is less than 25 and the
    modularity gain is greater than 0, assign the vertex to its neighbouring community"""
    max_q = 0
    best_community = vertex.community
    for neighbour in vertex.neighbours:
        community = graph.get_communities()[neighbour.community]
        delta_q = calculate_delta_q(community, vertex, m)

        if max_q < delta_q and len(community[0]) < 25:
            max_q = delta_q
            best_community = neighbour.community

    # If modularity gain is greater than 0, reassign communities
    if max_q > 0:
        neighbour_community = graph.get_communities()[best_community]
        old_community = graph.get_communities()[vertex.community]
        best_k_i_in = k_i_in(vertex, neighbour_community)
        best_k_i_out = k_i_out(vertex, old_community)
        graph.change_communities(vertex, best_community, best_k_i_in, best_k_i_out)
        vertex.community = best_community


def louvain(graph: movie_class.Network, epochs: int) -> None:
    """Modified Louvain's algorithm for community detection. Our algorithm follows phase 1
    of the Louvain's algorithm for a certain number of epochs to assign the movies in a graph
    to communities. Although the resulting graph might result in a lower overall modularity,
    we insist the size of a community is less than 25, in order to make more balanced calculations
    with respect to the dataset so the majority of the dataset doesn't fall under a single community."""
    m = m_func(graph)
    for _ in range(epochs):
        for vertex_name in graph.get_movies():
            louvain_helper(graph, graph.get_movies()[vertex_name], m)
    graph.remove_empty_communities()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['movie_class'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
