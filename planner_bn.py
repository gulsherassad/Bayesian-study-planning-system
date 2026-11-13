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
cpd_d1 = TabularCPD('Difficulty_C1', 2, [[0.4], [0.6]], state_names={'Difficulty_C1': ['easy', 'hard']})  # bayes rule: somewhat hard
cpd_d2 = TabularCPD('Difficulty_C2', 2, [[0.2], [0.8]], state_names={'Difficulty_C2': ['easy', 'hard']})  # inference: hard
cpd_d3 = TabularCPD('Difficulty_C3', 2, [[0.4], [0.6]], state_names={'Difficulty_C3': ['easy', 'hard']})  # expected utility: somewhat hard

# no reason to think one type of student is more common
cpd_level = TabularCPD('StudentLevel', 2, [[0.5], [0.5]], state_names={'StudentLevel': ['struggling', 'advanced']})

# few = 3 days or less until the exam
cpd_days = TabularCPD('DaysLeft', 2, [[0.5], [0.5]], state_names={'DaysLeft': ['few', 'many']})

# Pr(Mastery | Difficulty, StudentLevel)
# columns: easy+struggling, easy+advanced, hard+struggling, hard+advanced
# hard+struggling is my gut feeling for each concept, the rest follow from it:
# easy roughly doubles a struggling student's chance, advanced adds about 0.45

# bayes rule
cpd_m1 = TabularCPD('Mastery_C1', 2,
                    [[0.40, 0.05, 0.70, 0.25],   # low
                     [0.60, 0.95, 0.30, 0.75]],  # high
                    evidence=['Difficulty_C1', 'StudentLevel'], evidence_card=[2, 2],
                    state_names={'Mastery_C1': ['low', 'high'],
                                 'Difficulty_C1': ['easy', 'hard'],
                                 'StudentLevel': ['struggling', 'advanced']})

# inference, lower than the others everywhere since I find it the hardest
cpd_m2 = TabularCPD('Mastery_C2', 2,
                    [[0.55, 0.10, 0.90, 0.40],   # low
                     [0.45, 0.90, 0.10, 0.60]],  # high
                    evidence=['Difficulty_C2', 'StudentLevel'], evidence_card=[2, 2],
                    state_names={'Mastery_C2': ['low', 'high'],
                                 'Difficulty_C2': ['easy', 'hard'],
                                 'StudentLevel': ['struggling', 'advanced']})

# expected utility, same as bayes rule since I rated them the same
cpd_m3 = TabularCPD('Mastery_C3', 2,
                    [[0.40, 0.05, 0.70, 0.25],   # low
                     [0.60, 0.95, 0.30, 0.75]],  # high
                    evidence=['Difficulty_C3', 'StudentLevel'], evidence_card=[2, 2],
                    state_names={'Mastery_C3': ['low', 'high'],
                                 'Difficulty_C3': ['easy', 'hard'],
                                 'StudentLevel': ['struggling', 'advanced']})

# Pr(Stress | DaysLeft)
# columns: few, many
cpd_stress = TabularCPD('Stress', 2,
                        [[0.25, 0.75],   # low
                         [0.75, 0.25]],  # high
                        evidence=['DaysLeft'], evidence_card=[2],
                        state_names={'Stress': ['low', 'high'],
                                     'DaysLeft': ['few', 'many']})
# few days left: exam is close so most people are stressed
# many days left: plenty of time so most people are calm, some stress early anyway

# Pr(StudyNeed | Mastery_C1, Mastery_C2, Mastery_C3, DaysLeft)
# more low concepts and fewer days left = higher need
# column order: LLL few, LLL many, LLH few, LLH many, ... HHH few, HHH many
cpd_need = TabularCPD('StudyNeed', 3,
                      [[0.02, 0.10, 0.05, 0.20, 0.05, 0.20, 0.25, 0.50,
                        0.05, 0.20, 0.25, 0.50, 0.25, 0.50, 0.60, 0.80],   # low
                       [0.18, 0.40, 0.35, 0.50, 0.35, 0.50, 0.50, 0.40,
                        0.35, 0.50, 0.50, 0.40, 0.50, 0.40, 0.30, 0.15],   # medium
                       [0.80, 0.50, 0.60, 0.30, 0.60, 0.30, 0.25, 0.10,
                        0.60, 0.30, 0.25, 0.10, 0.25, 0.10, 0.10, 0.05]],  # high
                      evidence=['Mastery_C1', 'Mastery_C2', 'Mastery_C3', 'DaysLeft'],
                      evidence_card=[2, 2, 2, 2],
                      state_names={'StudyNeed': ['low', 'medium', 'high'],
                                   'Mastery_C1': ['low', 'high'],
                                   'Mastery_C2': ['low', 'high'],
                                   'Mastery_C3': ['low', 'high'],
                                   'DaysLeft': ['few', 'many']})

model.add_cpds(cpd_d1, cpd_d2, cpd_d3, cpd_level, cpd_days,
               cpd_m1, cpd_m2, cpd_m3, cpd_stress, cpd_need)
assert model.check_model()
print("model is valid")

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