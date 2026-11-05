from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import BeliefPropagation
import matplotlib.pyplot as plt
import networkx as nx

# concepts: C1 = Bayes rule, C2 = Bayes net inference, C3 = expected utility

model = DiscreteBayesianNetwork([
    ('Difficulty_C1', 'Mastery_C1'), ('StudentLevel', 'Mastery_C1'),
    ('Difficulty_C2', 'Mastery_C2'), ('StudentLevel', 'Mastery_C2'),
    ('Difficulty_C3', 'Mastery_C3'), ('StudentLevel', 'Mastery_C3'),
    ('Mastery_C1', 'StudyNeed'), ('Mastery_C2', 'StudyNeed'),
    ('Mastery_C3', 'StudyNeed'), ('DaysLeft', 'StudyNeed'),
    ('DaysLeft', 'Stress'), ('CalendarLoad', 'Stress'),
])

# difficulty priors, based on how hard I found each one
cpd_d1 = TabularCPD('Difficulty_C1', 2, [[0.6], [0.4]],
                    state_names={'Difficulty_C1': ['easy', 'hard']})  # bayes rule was ok
cpd_d2 = TabularCPD('Difficulty_C2', 2, [[0.3], [0.7]],
                    state_names={'Difficulty_C2': ['easy', 'hard']})  # inference was the hardest
cpd_d3 = TabularCPD('Difficulty_C3', 2, [[0.5], [0.5]],
                    state_names={'Difficulty_C3': ['easy', 'hard']})  # EU somewhere in between

# uniform since these will always be observed
cpd_level = TabularCPD('StudentLevel', 2, [[0.5], [0.5]],
                       state_names={'StudentLevel': ['struggling', 'advanced']})
cpd_days = TabularCPD('DaysLeft', 2, [[0.5], [0.5]],
                      state_names={'DaysLeft': ['few', 'many']})  # few = 3 days or less
cpd_cal = TabularCPD('CalendarLoad', 2, [[0.5], [0.5]],
                     state_names={'CalendarLoad': ['light', 'busy']})

# Pr(Mastery | Difficulty, StudentLevel), same numbers for all 3 concepts
# columns: easy+struggling, easy+advanced, hard+struggling, hard+advanced
mastery_values = [
    [0.55, 0.10, 0.85, 0.30],  # low
    [0.45, 0.90, 0.15, 0.70],  # high
]
# easy+struggling: about a coin flip
# easy+advanced: almost always mastered
# hard+struggling: usually not mastered yet
# hard+advanced: usually mastered but not always

cpd_m1 = TabularCPD('Mastery_C1', 2, mastery_values,
                    evidence=['Difficulty_C1', 'StudentLevel'], evidence_card=[2, 2],
                    state_names={'Mastery_C1': ['low', 'high'],
                                 'Difficulty_C1': ['easy', 'hard'],
                                 'StudentLevel': ['struggling', 'advanced']})
cpd_m2 = TabularCPD('Mastery_C2', 2, mastery_values,
                    evidence=['Difficulty_C2', 'StudentLevel'], evidence_card=[2, 2],
                    state_names={'Mastery_C2': ['low', 'high'],
                                 'Difficulty_C2': ['easy', 'hard'],
                                 'StudentLevel': ['struggling', 'advanced']})
cpd_m3 = TabularCPD('Mastery_C3', 2, mastery_values,
                    evidence=['Difficulty_C3', 'StudentLevel'], evidence_card=[2, 2],
                    state_names={'Mastery_C3': ['low', 'high'],
                                 'Difficulty_C3': ['easy', 'hard'],
                                 'StudentLevel': ['struggling', 'advanced']})

# Pr(Stress | DaysLeft, CalendarLoad)
# columns: few+light, few+busy, many+light, many+busy
cpd_stress = TabularCPD('Stress', 2,
                        [[0.45, 0.15, 0.85, 0.60],   # low
                         [0.55, 0.85, 0.15, 0.40]],  # high
                        evidence=['DaysLeft', 'CalendarLoad'], evidence_card=[2, 2],
                        state_names={'Stress': ['low', 'high'],
                                     'DaysLeft': ['few', 'many'],
                                     'CalendarLoad': ['light', 'busy']})
# few+light: exam is close so a bit stressed already
# few+busy: worst case, exam close and schedule packed
# many+light: lots of time, not stressed
# many+busy: time left but a busy week still adds stress

# Pr(StudyNeed | Mastery_C1, Mastery_C2, Mastery_C3, DaysLeft)
# 16 columns. I assumed study need only depends on how many concepts are low,
# not which ones. More low concepts and fewer days = higher need.
# column order: M1 M2 M3 Days (L = low, H = high)
#  LLL few, LLL many, LLH few, LLH many, LHL few, LHL many, LHH few, LHH many,
#  HLL few, HLL many, HLH few, HLH many, HHL few, HHL many, HHH few, HHH many
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
# 3 low: high need, even more if few days (0.80 vs 0.50)
# 2 low: mostly high if few days, medium if many
# 1 low: mostly medium
# 0 low: mostly low, but a quick review still helps if the exam is close

model.add_cpds(cpd_d1, cpd_d2, cpd_d3, cpd_level, cpd_days, cpd_cal,
               cpd_m1, cpd_m2, cpd_m3, cpd_stress, cpd_need)
assert model.check_model()


def draw_model():
    di_graph = nx.DiGraph(model.edges())
    pos = {'Difficulty_C1': (0, 3), 'Difficulty_C2': (2, 3), 'Difficulty_C3': (4, 3),
           'StudentLevel': (6, 3), 'Mastery_C1': (0, 2), 'Mastery_C2': (2, 2),
           'Mastery_C3': (4, 2), 'DaysLeft': (6, 2), 'CalendarLoad': (8, 2),
           'StudyNeed': (3, 1), 'Stress': (7, 1)}
    plt.figure(figsize=(12, 6))
    nx.draw(di_graph, pos, with_labels=True, node_size=4500, node_color='skyblue',
            edgecolors='black', font_size=8, font_weight='bold', edge_color='gray',
            width=2, arrows=True, arrowsize=20)
    plt.title("Bayesian Study Planner Network")
    plt.axis('off')
    plt.savefig('network.png')
    plt.show()


if __name__ == '__main__':
    inference = BeliefPropagation(model)
    evidence = {'StudentLevel': 'struggling', 'Difficulty_C1': 'hard',
                'Difficulty_C2': 'hard', 'Difficulty_C3': 'hard',
                'DaysLeft': 'few', 'CalendarLoad': 'busy'}
    print(inference.query(variables=['StudyNeed'], evidence=evidence))
    print(inference.query(variables=['Stress'], evidence=evidence))
    # draw_model()