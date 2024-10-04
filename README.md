## Movie Recommendation System

Project developed by Fiona Verzivolli, Andrew Sasmito, Saahil Kapasi, and Naoroj Farhan.
This project implements a movie recommendation system that leverages Louvain's Algorithm for graph community detection to provide personalized movie suggestions based on user preferences and interactions. 

### Key Features

- **Advanced Recommendation Engine**: Utilizes Louvain's Algorithm, a state-of-the-art method for detecting communities within large networks, to identify groups of similar movies. This enhances the accuracy and relevance of recommendations.

- **Core Technologies**:
  - **Python**: The backbone of the system, Python is used for all core logic and computational tasks, ensuring robust performance and easy integration with other tools.
  - **NetworkX**: A powerful library for the creation, manipulation, and study of complex networks. It is used here to handle graph data structures and perform clustering operations essential for the recommendation process.
  - **Tkinter**: Provides a user-friendly graphical interface that allows users to interact with the recommendation system easily. The GUI includes features like movie search, viewing recommendations, and user preference input.

- **User Interaction**:
  - **Preference-Based Recommendations**: Users can input their movie preferences and past interactions, which the system uses to tailor its recommendations.
  - **Dynamic Updates**: The recommendation engine continuously updates its suggestions based on new user data, ensuring that recommendations remain relevant over time.

### Installation and Usage

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/movierecommendation.git
    cd movierecommendation
    ```

2. **Install Dependencies**:
    Make sure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```bash
    python main.py
    ```

4. **Interact with the GUI**:
    - Use the provided Tkinter interface to input your movie preferences.
    - View the recommended movies based on your input and interactions.

### Technical Details

- **Graph Community Detection**: The Louvain Algorithm is a heuristic method that is efficient in detecting communities in large networks, making it ideal for this recommendation system. The algorithm works by optimizing the modularity of a partition of the network.
- **Graph Representation**: Movies and user interactions are represented as nodes and edges in a graph. This structure allows for the identification of clusters of similar movies.
- **User-Friendly Interface**: The Tkinter-based GUI is designed to be intuitive, ensuring that users of all technical levels can easily navigate and utilize the system.

### Contributions

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or bug reports.

---
