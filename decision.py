from pgmpy.inference import BeliefPropagation
from planner_bn import model

actions = ['intense', 'light', 'rest']
# intense = 5 hour study block, light = 1 hour review, rest = clear the day


def util(need, stress, action):
    """
    Utility of an action given study need and stress, in [-10, +10]
    first part is about exam success, second part is about stress
    """
    val = 0

    # exam success part: does the action match how much studying is needed
    if need == 'high':
        if action == 'intense':
            val = val + 6
        elif action == 'light':
            val = val + 1
        else:
            val = val - 6   # resting when you really need to study hurts the exam
    elif need == 'medium':
        if action == 'intense':
            val = val + 2
        elif action == 'light':
            val = val + 4
        else:
            val = val - 2
    else:  # low
        if action == 'intense':
            val = val - 1   # wasted time, would be better spent resting
        elif action == 'light':
            val = val + 2
        else:
            val = val + 4

    # stress part: intense blocks make stress worse, rest helps
    if stress == 'high':
        if action == 'intense':
            val = val - 4
        elif action == 'light':
            val = val - 1
        else:
            val = val + 3
    else:  # low
        if action == 'intense':
            val = val - 1
        elif action == 'rest':
            val = val + 1

    return val


def get_meu_action(evidence):
    inference = BeliefPropagation(model)
    pr_need = inference.query(variables=['StudyNeed'], evidence=evidence)
    pr_stress = inference.query(variables=['Stress'], evidence=evidence)

    # StudyNeed and Stress are independent once DaysLeft is observed,
    # so Pr(need, stress) = Pr(need) * Pr(stress)
    eu = {}
    for action in actions:
        eu[action] = 0.0
        for need in ['low', 'medium', 'high']:
            for stress in ['low', 'high']:
                p = pr_need.get_value(StudyNeed=need) * pr_stress.get_value(Stress=stress)
                eu[action] = eu[action] + p * util(need, stress, action)

    # MEU principle: pick the action with the highest expected utility
    best = max(eu, key=eu.get)
    return best, eu


if __name__ == '__main__':
    struggling = {'StudentLevel': 'struggling', 'Difficulty_C1': 'hard',
                  'Difficulty_C2': 'hard', 'Difficulty_C3': 'hard',
                  'DaysLeft': 'few', 'CalendarLoad': 'light'}
    advanced = {'StudentLevel': 'advanced', 'Difficulty_C1': 'easy',
                'Difficulty_C2': 'easy', 'Difficulty_C3': 'easy',
                'DaysLeft': 'few', 'CalendarLoad': 'light'}

    for name, evidence in [('struggling', struggling), ('advanced', advanced)]:
        best, eu = get_meu_action(evidence)
        print(name)
        for action in actions:
            print(f"  EU({action}) = {eu[action]:.2f}")
        print("  best action:", best)