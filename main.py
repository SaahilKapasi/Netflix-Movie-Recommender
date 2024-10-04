"""CSC111 Project 2: Netflix Movie Recommendation System

This is the main file of the Netflix Movie Recommendation System.
"""
from load_graph import load_movie_graph
from clustering import louvain
import tkinter as tk
from front import TkinterApp


if __name__ == "__main__":
    print("Loading GUI... Please be patient :) The graph is being loaded and clustered.")
    graph = load_movie_graph('data/shuffled_user_ratings.csv', 'data/movies.csv')
    louvain(graph, 3)
    app = TkinterApp(tk.Tk(), graph)
    app.run()
