from planner_bn import model

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

if __name__ == '__main__':
    for need in ['low', 'medium', 'high']:
        for stress in ['low', 'high']:
            print(need, stress, [util(need, stress, a) for a in actions])