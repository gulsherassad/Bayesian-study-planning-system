import matplotlib.pyplot as plt
from decision import get_meu_action, actions

# each scenario changes the student type and how hard the 3 concepts are
scenarios = {
    'Struggling, all hard': {'StudentLevel': 'struggling', 'Difficulty_C1': 'hard',
                             'Difficulty_C2': 'hard', 'Difficulty_C3': 'hard',
                             'DaysLeft': 'few', 'CalendarLoad': 'light'},
    'Struggling, all easy': {'StudentLevel': 'struggling', 'Difficulty_C1': 'easy',
                             'Difficulty_C2': 'easy', 'Difficulty_C3': 'easy',
                             'DaysLeft': 'few', 'CalendarLoad': 'light'},
    'Advanced, all hard': {'StudentLevel': 'advanced', 'Difficulty_C1': 'hard',
                           'Difficulty_C2': 'hard', 'Difficulty_C3': 'hard',
                           'DaysLeft': 'few', 'CalendarLoad': 'light'},
    'Advanced, all easy': {'StudentLevel': 'advanced', 'Difficulty_C1': 'easy',
                           'Difficulty_C2': 'easy', 'Difficulty_C3': 'easy',
                           'DaysLeft': 'few', 'CalendarLoad': 'light'},
    # same as above but only inference (C2) is hard, then a busy calendar
    'Advanced, C2 hard, light week': {'StudentLevel': 'advanced', 'Difficulty_C1': 'easy',
                                      'Difficulty_C2': 'hard', 'Difficulty_C3': 'easy',
                                      'DaysLeft': 'few', 'CalendarLoad': 'light'},
    'Advanced, C2 hard, busy week': {'StudentLevel': 'advanced', 'Difficulty_C1': 'easy',
                                     'Difficulty_C2': 'hard', 'Difficulty_C3': 'easy',
                                     'DaysLeft': 'few', 'CalendarLoad': 'busy'},
}

results = {}
for name in scenarios:
    best, eu = get_meu_action(scenarios[name])
    results[name] = eu
    print(name)
    for action in actions:
        print(f"  EU({action}) = {eu[action]:.2f}")
    print("  best action:", best)
    print()

# bar chart of EU for each action in each scenario
names = list(scenarios.keys())
x = range(len(names))
width = 0.25
plt.figure(figsize=(12, 6))
for i, action in enumerate(actions):
    values = [results[name][action] for name in names]
    plt.bar([pos + i * width for pos in x], values, width, label=action)
plt.xticks([pos + width for pos in x], names, rotation=20, ha='right')
plt.axhline(0, color='black', linewidth=0.8)
plt.ylabel('Expected utility')
plt.title('Expected utility of each action by scenario')
plt.legend()
plt.tight_layout()
plt.savefig('scenarios.png')
plt.show()