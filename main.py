from datetime import datetime, timedelta
from decision import get_meu_action, actions
from calendar_api import get_service, schedule_action, tz

print("Bayesian Study Planner")
print("C1 = Bayes' rule, C2 = Bayes net inference, C3 = expected utility")
print()

today = datetime.now(tz).date()

# can enter more than one exam, it plans for the closest one
dates = input("Exam dates (YYYY-MM-DD, separate with commas): ")
exams = []
for d in dates.split(','):
    exam = datetime.strptime(d.strip(), '%Y-%m-%d').date()
    if exam > today:
        exams.append(exam)
exam = min(exams)
print("Planning for the exam on", exam)

level = input("Struggling or advanced? ")
d1 = input("How hard is C1 for you? (easy/hard) ")
d2 = input("How hard is C2 for you? (easy/hard) ")
d3 = input("How hard is C3 for you? (easy/hard) ")

service = get_service()
print()

# plan every day from today until the day before the exam
days = (exam - today).days
for i in range(days):
    day = today + timedelta(days=i)
    left = days - i

    # few = 3 days or less
    if left <= 3:
        days_left = 'few'
    else:
        days_left = 'many'

    evidence = {'StudentLevel': level, 'Difficulty_C1': d1, 'Difficulty_C2': d2,
                'Difficulty_C3': d3, 'DaysLeft': days_left}
    best, eu = get_meu_action(evidence)

    scores = ', '.join(f"{a} {eu[a]:.2f}" for a in actions)
    print(f"{day} ({left} days left): {best}   [{scores}]")
    schedule_action(service, best, day)