from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import BeliefPropagation
import matplotlib.pyplot as plt
import networkx as nx

# Concepts I'm modelling (from COSC 329):
# C1 = Bayes rule, C2 = Bayes net inference, C3 = expected utility

# Structure of the network
model = DiscreteBayesianNetwork([
    # each concept's mastery depends on how hard it is and the type of student
    ('Difficulty_C1', 'Mastery_C1'), ('StudentLevel', 'Mastery_C1'),
    ('Difficulty_C2', 'Mastery_C2'), ('StudentLevel', 'Mastery_C2'),
    ('Difficulty_C3', 'Mastery_C3'), ('StudentLevel', 'Mastery_C3'),
    # how much studying is needed depends on mastery and time left
    ('Mastery_C1', 'StudyNeed'), ('Mastery_C2', 'StudyNeed'),
    ('Mastery_C3', 'StudyNeed'), ('DaysLeft', 'StudyNeed'),
    # stress depends on time left and how busy my calendar is
    ('DaysLeft', 'Stress'), ('CalendarLoad', 'Stress'),
])


def draw_model(model):
    di_graph = nx.DiGraph(model.edges())
    # fixed positions so the graph reads top to bottom
    pos = {
        'Difficulty_C1': (0, 3), 'Difficulty_C2': (2, 3), 'Difficulty_C3': (4, 3),
        'StudentLevel': (6, 3),
        'Mastery_C1': (0, 2), 'Mastery_C2': (2, 2), 'Mastery_C3': (4, 2),
        'DaysLeft': (6, 2), 'CalendarLoad': (8, 2),
        'StudyNeed': (3, 1), 'Stress': (7, 1),
    }
    plt.figure(figsize=(12, 6))
    nx.draw(
        di_graph, pos,
        with_labels=True,
        node_size=4500,
        node_color='skyblue',
        edgecolors='black',
        font_size=8,
        font_weight='bold',
        edge_color='gray',
        width=2,
        arrows=True,
        arrowsize=20,
    )
    plt.title("Bayesian Study Planner Network", fontsize=14, pad=20)
    plt.axis('off')
    plt.savefig('network.png')
    plt.show()


if __name__ == '__main__':
    print("Nodes:", len(model.nodes()))
    draw_model(model)