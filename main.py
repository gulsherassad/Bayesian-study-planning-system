from datetime import datetime
from decision import get_meu_action, actions
from calendar_api import get_service, schedule_action, tz

print("Bayesian Study Planner")
print("C1 = Bayes' rule, C2 = Bayes net inference, C3 = expected utility")
print()

exam_date = input("Exam date (YYYY-MM-DD): ")
exam = datetime.strptime(exam_date, '%Y-%m-%d').date()
days = (exam - datetime.now(tz).date()).days
print("Days until exam:", days)

# few = 3 days or less
if days <= 3:
    days_left = 'few'
else:
    days_left = 'many'

level = input("Struggling or advanced? ")
d1 = input("How hard is C1 for you? (easy/hard) ")
d2 = input("How hard is C2 for you? (easy/hard) ")
d3 = input("How hard is C3 for you? (easy/hard) ")

evidence = {'StudentLevel': level, 'Difficulty_C1': d1, 'Difficulty_C2': d2,
            'Difficulty_C3': d3, 'DaysLeft': days_left}

best, eu = get_meu_action(evidence)
print()
for action in actions:
    print(f"EU({action}) = {eu[action]:.2f}")
print("Best action:", best)

service = get_service()
schedule_action(service, best)