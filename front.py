"""CSC111 Project 2: Netflix Movie Recommendation System

This is the frontend file of the Netflix Movie Recommendation System.
It is responsible for setting up and handling the Tkinter GUI.
"""
import tkinter as tk
from typing import Any
import movie_class
from visualization import visualize_weighted_graph


class TkinterApp:
    """Class that stores all of our information for the frontend interface.
    This includes the initialization (creating our window and tkinter widgets), as
    well as the methods needed to make our frontend interactive."""
    selected_movies: set
    list_of_movies: list
    root: tk.Tk
    movies: tk.Listbox
    movie_entry: tk.Entry
    spinbox: tk.Spinbox
    selected_movies_listbox: tk.Listbox
    graph: movie_class.Network
    movie_recommendations: tk.Listbox

    def __init__(self, window_root: tk.Tk, graph: movie_class.Network) -> None:
        """Function to create our user interface window. Includes all tkinter widgets."""
        self.graph = graph
        self.selected_movies = set()
        self.list_of_movies = list(self.graph.get_movies().keys())
        self.root = window_root
        self.root.configure(background='#3B3B3B')

        self.root.geometry("1920x1080")  # initialize window
        self.root.title("Project 2 Window")
        label = tk.Label(self.root, text="Movie Recommender", font=('Courier New', 80), bg='#3B3B3B', fg="white")
        label.pack(padx=20, pady=20)
        label2 = tk.Label(self.root,
                          text="To begin, enter a movie you have watched or like, \nand your desired number of reviews",
                          font=('Courier New', 25), bg='#3B3B3B', fg="white")
        label2.pack(padx=20, pady=10)

        movie_input1 = tk.Label(self.root, text="Selected Movies", font=('Courier New', 20), bg='#3B3B3B', fg="white")
        movie_input1.pack()

        self.selected_movies_listbox = tk.Listbox(self.root, width=50, height=5, selectmode='single')  # create dropdown
        self.selected_movies_listbox.pack(pady=5)

        movie_input2 = tk.Label(self.root, text="Start typing to find your movie, and then click on it.",
                                font=('Courier New', 20), bg='#3B3B3B', fg="white")
        movie_input2.pack(pady=5)

        self.movie_entry = tk.Entry(self.root, font=('Courier New', 20))
        self.movie_entry.pack(pady=5)

        self.movie_entry.bind("<KeyRelease>", self.verify)

        self.movies = tk.Listbox(self.root, width=50, height=5)
        self.movies.pack(pady=5)

        movie_input3 = tk.Label(self.root, text="Maximum number of recommendations (1-5)", font=('Courier', 20),
                                bg='#3B3B3B', fg="white")
        movie_input3.pack(pady=5)

        self.spinbox = tk.Spinbox(self.root, from_=1, to=5)  # create input for # of reviews
        self.spinbox.pack(padx=20, pady=5)

        # update our box of selected movies to include the movie we selected in our selection box
        self.selected_movies_listbox.bind("<<ListboxSelect>>", self.update_selected_movies)

        button = tk.Button(self.root, text="Recommend", font=('Courier New', 30), command=self.recommend_movies)
        button.pack()

        self.modify(self.list_of_movies)

        self.movies.bind("<<ListboxSelect>>", self.updater)  # selecting a movie will trigger the updater function

        # initialize the movie_recommendations listbox
        self.movie_recommendations = tk.Listbox(self.root, width=50, height=5)
        self.movie_recommendations.pack(pady=5)

    def updater(self, event: tk.Event) -> None:
        """Replace entered text with selected movie and store it.
        Raise an error if the user selected too many movies."""
        if self.movies.curselection():  # check if there already is a selection
            index = self.movies.curselection()[0]
            movie_name = self.movies.get(index)  # if so, get currently selected item
            self.movie_entry.delete(0, tk.END)  # delete all movies
            self.movie_entry.insert(0, movie_name)  # insert current movie to our entries
            self.selected_movies.add(movie_name)  # add selected movie to selected_movies
            self.update_selected_movies()  # update selected movies

    def modify(self, lst: list) -> Any:
        """Initially display all movie options in our dropdown menu"""
        if not self.movie_entry.get():  # make our dropdown empty at first
            return
        self.movies.delete(0, tk.END)  # clear dropdown menu so it updates
        for movie in lst:
            self.movies.insert(tk.END, movie)  # add each movie

    def verify(self, event: tk.Event) -> Any:
        """Match the user's text to movie titles in our movies.csv file"""
        if self.movie_entry.get() != '':  # if there is text,
            lst = []
            for i in self.list_of_movies:
                correct = self.movie_entry.get()
                if correct.lower() in i.lower():
                    lst.append(i)  # add each corresponding movie to lst
            self.modify(lst)  # update

    def display_recommendations(self, movie_list: list) -> None:
        """Add the recommendations to our GUI"""
        self.movie_recommendations.delete(0, tk.END)
        for movie in movie_list[:int(self.spinbox.get())]:
            self.movie_recommendations.insert(0, movie)

    def recommend_movies(self) -> None:
        """Function to update recommended movies when recommended is pressed
        and reset several visual elements."""
        recommendations = self.graph.get_best_movies(list(self.selected_movies), 5)
        self.display_recommendations(recommendations)
        visualize_weighted_graph(self.graph, list(self.selected_movies))
        self.movie_entry.delete(0, tk.END)  # clear search bar
        self.selected_movies_listbox.delete(0, tk.END)  # clear selected movies box
        self.selected_movies = set()  # empty selected movies set
        self.movies.selection_clear(0, tk.END)  # need to clear selection in movies listbox

    def update_selected_movies(self, event: tk.Event = None) -> None:
        """Insert the movies the user selected to our box of selected movies"""
        self.selected_movies_listbox.delete(0, tk.END)  # clear our selected movies at first
        for movie in self.selected_movies:  # after clearing,
            self.selected_movies_listbox.insert(tk.END, movie)

    def run(self) -> None:
        """Run the GUI"""
        self.root.mainloop()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'tkinter', 'movie_class', 'visualization'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
