from planner_bn import model
from pgmpy.inference import BeliefPropagation

# intense = 5 hour study block today
# practice = 2 hour practice problem session
# light = 1 hour review session
# rest = clear the calendar for a rest day
actions = ['intense', 'practice', 'light', 'rest']

def util(need, stress, action):
    # utility from -10 to +10
    # part 1 is exam success, part 2 is stress
    val = 0

    # exam success: does the action match how much studying is needed
    if need == 'high':
        if action == 'intense':
            val = val + 8
        elif action == 'practice':
            val = val + 3
        elif action == 'rest':
            val = val - 6
    elif need == 'medium':
        if action == 'practice':
            val = val + 4
        elif action == 'light':
            val = val + 3
        elif action == 'rest':
            val = val - 2
    else:
        if action == 'intense':
            val = val - 3
        elif action == 'practice':
            val = val - 1
        elif action == 'light':
            val = val + 2
        else:
            val = val + 4

    # stress: big study blocks make stress worse, rest helps
    if stress == 'high':
        if action == 'intense':
            val = val - 3
        elif action == 'practice':
            val = val - 1
        elif action == 'rest':
            val = val + 2

    return val

def get_meu_action(evidence):
    inference = BeliefPropagation(model)
    pr_need = inference.query(variables=['StudyNeed'], evidence=evidence)
    pr_stress = inference.query(variables=['Stress'], evidence=evidence)

    # EU(action) = sum of Pr(need) * Pr(stress) * U(need, stress, action)
    # need and stress are independent once DaysLeft is observed
    eu = {}
    for action in actions:
        eu[action] = 0
        for need in ['low', 'medium', 'high']:
            for stress in ['low', 'high']:
                p = pr_need.get_value(StudyNeed=need) * pr_stress.get_value(Stress=stress)
                eu[action] = eu[action] + p * util(need, stress, action)

    # pick the action with the highest EU
    best = max(eu, key=eu.get)
    return best, eu

if __name__ == '__main__':
    struggling = {'StudentLevel': 'struggling', 'Difficulty_C1': 'hard',
                  'Difficulty_C2': 'hard', 'Difficulty_C3': 'hard', 'DaysLeft': 'few'}
    advanced = {'StudentLevel': 'advanced', 'Difficulty_C1': 'easy',
                'Difficulty_C2': 'easy', 'Difficulty_C3': 'easy', 'DaysLeft': 'many'}

    for name, evidence in [('struggling', struggling), ('advanced', advanced)]:
        best, eu = get_meu_action(evidence)
        print(name)
        for action in actions:
            print(f"  EU({action}) = {eu[action]:.2f}")
        print("  best:", best)