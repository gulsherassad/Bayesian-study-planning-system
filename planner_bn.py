from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
import matplotlib.pyplot as plt
import networkx as nx

# C1 = bayes rule, C2 = bayes net inference, C3 = expected utility

# difficulty and student level affect mastery of each concept
# mastery and days left affect how much studying is needed
# days left affects stress
model = DiscreteBayesianNetwork([
    ('Difficulty_C1', 'Mastery_C1'),
    ('Difficulty_C2', 'Mastery_C2'),
    ('Difficulty_C3', 'Mastery_C3'),
    ('StudentLevel', 'Mastery_C1'),
    ('StudentLevel', 'Mastery_C2'),
    ('StudentLevel', 'Mastery_C3'),
    ('Mastery_C1', 'StudyNeed'),
    ('Mastery_C2', 'StudyNeed'),
    ('Mastery_C3', 'StudyNeed'),
    ('DaysLeft', 'StudyNeed'),
    ('DaysLeft', 'Stress'),
])

# root nodes, these will be set as evidence so the priors are just my guesses
# state order: [easy, hard]
cpd_d1 = TabularCPD('Difficulty_C1', 2, [[0.4], [0.6]],
                    state_names={'Difficulty_C1': ['easy', 'hard']})  # bayes rule: somewhat hard
cpd_d2 = TabularCPD('Difficulty_C2', 2, [[0.2], [0.8]],
                    state_names={'Difficulty_C2': ['easy', 'hard']})  # inference: hard
cpd_d3 = TabularCPD('Difficulty_C3', 2, [[0.4], [0.6]],
                    state_names={'Difficulty_C3': ['easy', 'hard']})  # expected utility: somewhat hard

# no reason to think one type of student is more common
cpd_level = TabularCPD('StudentLevel', 2, [[0.5], [0.5]],
                       state_names={'StudentLevel': ['struggling', 'advanced']})

# few = 3 days or less until the exam
cpd_days = TabularCPD('DaysLeft', 2, [[0.5], [0.5]],
                      state_names={'DaysLeft': ['few', 'many']})

# draw the network (same as the class example)
di_graph = nx.DiGraph(model.edges())

# spring_layout made it messy so I placed the nodes in rows myself
pos = {
    'Difficulty_C1': (0, 2), 'Difficulty_C2': (2, 2), 'Difficulty_C3': (4, 2), 'StudentLevel': (6, 2),
    'Mastery_C1': (0, 1), 'Mastery_C2': (2, 1), 'Mastery_C3': (4, 1), 'DaysLeft': (6, 1),
    'StudyNeed': (3, 0), 'Stress': (6, 0),
}

plt.figure(figsize=(12, 6))
nx.draw(
    di_graph,
    pos,
    with_labels=True,
    node_size=4500,
    node_color='skyblue',
    edgecolors='black',
    font_size=8,
    font_weight='bold',
    edge_color='gray',
    width=2,
    arrows=True,
    arrowsize=20
)
plt.title("Study Planner Bayes Net")
plt.axis('off')
plt.savefig('network.png')
plt.show()