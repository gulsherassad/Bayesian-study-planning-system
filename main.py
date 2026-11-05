from datetime import datetime
from decision import get_meu_action, actions
from calendar_api import get_service, get_calendar_load, schedule_action, tz

print("Bayesian Study Planner")
print("C1 = Bayes rule, C2 = Bayes net inference, C3 = expected utility\n")

# exam date -> DaysLeft
exam_date = input("Exam date (YYYY-MM-DD): ")
exam = datetime.strptime(exam_date, '%Y-%m-%d').date()
days = (exam - datetime.now(tz).date()).days
print("Days until exam:", days)
if days <= 3:
    days_left = 'few'
else:
    days_left = 'many'

# student info
level = input("Are you struggling or advanced? ")
d1 = input("How hard is C1 for you? (easy/hard) ")
d2 = input("How hard is C2 for you? (easy/hard) ")
d3 = input("How hard is C3 for you? (easy/hard) ")

# check how busy my real calendar is
service = get_service()
calendar_load = get_calendar_load(service)
print("Calendar load:", calendar_load)

evidence = {'StudentLevel': level, 'Difficulty_C1': d1, 'Difficulty_C2': d2,
            'Difficulty_C3': d3, 'DaysLeft': days_left, 'CalendarLoad': calendar_load}

best, eu = get_meu_action(evidence)
print()
for action in actions:
    print(f"EU({action}) = {eu[action]:.2f}")
print("Best action:", best)

schedule_action(service, best)