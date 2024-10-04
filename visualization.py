"""CSC111 Project 2: Netflix Movie Recommendation System

This is the graph implementation file of the Netflix Movie Recommendation System.
"""
import colorsys
import networkx as nx
from plotly.graph_objs import Scatter, Figure
import movie_class


def generate_color_scheme(graph: movie_class.Network) -> dict[str, str]:
    """
    Generate random colours
    """
    colors = {}
    i = 0
    for community in graph.get_communities():
        hue = i / len(graph.get_communities())  # Varying the hue across the color spectrum
        lightness = 0.5  # You can adjust lightness if needed
        saturation = 0.7  # You can adjust saturation if needed
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        hex_color = f'#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}'
        colors[community] = hex_color
        i += 1

    return colors


def generate_graph_nx(graph: movie_class.Network, movie_names: list[str]) -> nx.classes.Graph():
    """
    Generate the networkx graph
    """
    graph_nx = nx.Graph()
    movies = graph.get_movies()
    visited, communities = set(), set()
    for movie in movie_names:
        graph_nx.add_node(movie, kind=movies[movie].community)
        communities.add(movies[movie].community)

    for movie in movies:
        if movies[movie].community in communities:
            graph_nx.add_node(movie, kind=movies[movie].community)

    for movie in movies:
        if movies[movie].community not in communities:
            continue
        visited.add(movies[movie])
        for neighbour in movies[movie].neighbours:
            if (neighbour not in visited and movies[movie].community in communities and neighbour.
                    community == movies[movie].community):
                graph_nx.add_edge(neighbour.title, movies[movie].title)
    return graph_nx


def setup_graph(graph: movie_class.Network,
                movie_names: list[str],
                layout: str = 'spring_layout') -> list:
    """Use plotly and networkx to setup the visuals for the given graph.

    Optional arguments:
        - weighted: True when weight data should be visualized
    """

    # Creating the graph
    graph_nx = generate_graph_nx(graph, movie_names)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    kinds = [graph_nx.nodes[k]['kind'] for k in graph_nx.nodes]

    # Generating the colours
    possible_colours = generate_color_scheme(graph)
    colours = [possible_colours[kind] for kind in kinds]

    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker={"symbol": 'circle-dot', "size": 10, "color": colours,
                             "line": {"color": 'rgb(50,50,50)', "width": 0.5}},
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    return [trace4]


def visualize_weighted_graph(graph: movie_class.Network,
                             movies: list[str],
                             layout: str = 'spring_layout',
                             output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given weighted graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """

    data = setup_graph(graph, movies, layout)
    draw_graph(data, output_file)


def draw_graph(data: list, output_file: str = '') -> None:
    """
    Draw graph based on given data.

    Optional arguments:
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
        - weight_positions: weights to draw on edges for a weighted graph
    """

    fig = Figure(data=data)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['movie_class', 'networkx', 'plotly.graph_objs',
                          'colorsys'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })

    # graph = load_graph.load_movie_graph('data/shuffled_user_ratings.csv', 'data/movies.csv', 10, 10000)
    # print('a')
    # clustering.louvain(graph, 3)
    # print('b')
    # visualize_weighted_graph(graph, movies=['Dinosaur Planet'])
    # print('C')
