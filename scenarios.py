import matplotlib.pyplot as plt
from decision import get_meu_action, actions

scenarios = {
    'Struggling\nall hard\nexam soon': {'StudentLevel': 'struggling', 'Difficulty_C1': 'hard',
                                        'Difficulty_C2': 'hard', 'Difficulty_C3': 'hard', 'DaysLeft': 'few'},
    'Struggling\nall easy\nexam soon': {'StudentLevel': 'struggling', 'Difficulty_C1': 'easy',
                                        'Difficulty_C2': 'easy', 'Difficulty_C3': 'easy', 'DaysLeft': 'few'},
    'Struggling\nall easy\nexam far': {'StudentLevel': 'struggling', 'Difficulty_C1': 'easy',
                                       'Difficulty_C2': 'easy', 'Difficulty_C3': 'easy', 'DaysLeft': 'many'},
    'Advanced\nall hard\nexam soon': {'StudentLevel': 'advanced', 'Difficulty_C1': 'hard',
                                      'Difficulty_C2': 'hard', 'Difficulty_C3': 'hard', 'DaysLeft': 'few'},
    'Advanced\nonly C2 hard\nexam soon': {'StudentLevel': 'advanced', 'Difficulty_C1': 'easy',
                                          'Difficulty_C2': 'hard', 'Difficulty_C3': 'easy', 'DaysLeft': 'few'},
    'Advanced\nall easy\nexam soon': {'StudentLevel': 'advanced', 'Difficulty_C1': 'easy',
                                      'Difficulty_C2': 'easy', 'Difficulty_C3': 'easy', 'DaysLeft': 'few'},
}

results = {}
for name in scenarios:
    best, eu = get_meu_action(scenarios[name])
    results[name] = eu
    print(name.replace('\n', ', '), '->', best)

# grouped bar chart, one group per scenario
names = list(scenarios.keys())
width = 0.2
plt.figure(figsize=(12, 6))
for i, action in enumerate(actions):
    x = [j + i * width for j in range(len(names))]
    y = [results[name][action] for name in names]
    plt.bar(x, y, width, label=action)
plt.xticks([j + 1.5 * width for j in range(len(names))], names)
plt.axhline(0, color='black', linewidth=0.8)
plt.ylabel('Expected utility')
plt.title('Expected utility of each action by scenario')
plt.legend()
plt.tight_layout()
plt.savefig('scenarios.png')
plt.show()