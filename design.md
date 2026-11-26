# Network Design

## Concepts (3 topics covered on the exam)
- C1: Bayes' rule - somewhat hard. I understand how to use the formula, but I sometimes struggle with understanding how new evidence changes the probability of something.
- C2: Bayes net inference - hard. I understand the basic idea, but I find it difficult to work through the inference process and understand how evidence affects different variables in the network.
- C3: Expected utility - somewhat hard. I understand that expected utility helps compare different actions, but I sometimes struggle with how utility values are assigned and how to calculate which action is the best choice.

## Variables
| Variable | Values | Type |
|---|---|---|
| Difficulty_C1, C2, C3 | easy, hard | observed |
| StudentLevel | struggling, advanced | observed |
| Mastery_C1, C2, C3 | low, high | hidden |
| DaysLeft | few (3 days or less), many | observed |
| Stress | low, high | hidden, query |
| StudyNeed | low, medium, high | hidden, query |

## Arrows
- Difficulty_Ci -> Mastery_Ci (harder concepts are less likely to be mastered)
- StudentLevel -> Mastery_C1, C2, C3 (stronger students master more)
- Mastery_C1, C2, C3 -> StudyNeed (lower mastery means more studying needed)
- DaysLeft -> StudyNeed (less time means more studying needed today)
- DaysLeft -> Stress (exam getting closer means more stress)

## Query
Pr(StudyNeed) and Pr(Stress) given the observed variables.
These go into the utility function to pick the best action.

## Actions
- intense: 5 hour study block today
- practice: 2 hour practice problem session
- light: 1 hour review session
- rest: clear the calendar for a rest day

## CPTs
### Root nodes
These are always set as evidence in the scenarios, so the priors only matter if a value is unknown.
- Difficulty_C1 (Bayes' rule): P(hard) = 0.6, because I rated it somewhat hard
- Difficulty_C2 (inference): P(hard) = 0.8, because I rated it hard
- Difficulty_C3 (expected utility): P(hard) = 0.6, because I rated it somewhat hard
- StudentLevel: 50/50, no reason to think one type of student is more common
- DaysLeft: 50/50, few = 3 days or less until the exam

### Mastery: Pr(Mastery | Difficulty, StudentLevel)
Chance the student has mastered each concept:

Bayes' rule (C1)
- easy, struggling: 0.60
- easy, advanced: 0.95
- hard, struggling: 0.30
- hard, advanced: 0.75

Inference (C2)
- easy, struggling: 0.45
- easy, advanced: 0.90
- hard, struggling: 0.10
- hard, advanced: 0.60

Expected utility (C3)
- same as Bayes' rule, since I rated them the same

How I picked these:
- hard + struggling is my gut feeling for each concept. Inference is the lowest because I find it the hardest.
- The rest follow a simple rule: an easy version roughly doubles a struggling student's chance, and an advanced student adds about 0.45.
- Inference is lower in every case because I think it's harder even when it's rated easy.
- No 0s or 1s, so evidence can always change the belief.
- Possible issue: student level matters more than difficulty here. I'll check in the scenarios that difficulty still changes the action.

### Stress: Pr(Stress | DaysLeft)
Chance of high stress:
- few days left: 0.75, the exam is close so most people are stressed, but not everyone
- many days left: 0.25, there's plenty of time so most people are calm, but some people stress early anyway

### StudyNeed: Pr(StudyNeed | Mastery_C1, Mastery_C2, Mastery_C3, DaysLeft)
This one has 16 columns. To keep it manageable, I assumed study need only depends on how many concepts are low mastery, not which ones. That leaves 8 cases.

Chance of low / medium / high need:
- 3 low, few days: 0.02 / 0.18 / 0.80, weak at everything and the exam is close
- 3 low, many days: 0.10 / 0.40 / 0.50, still high need but there's time
- 2 low, few days: 0.05 / 0.35 / 0.60, mostly high
- 2 low, many days: 0.20 / 0.50 / 0.30, mostly medium
- 1 low, few days: 0.25 / 0.50 / 0.25, mostly medium
- 1 low, many days: 0.50 / 0.40 / 0.10, low to medium
- 0 low, few days: 0.60 / 0.30 / 0.10, mostly low, but a quick review still helps
- 0 low, many days: 0.80 / 0.15 / 0.05, barely need to study

General rule: more low concepts and fewer days left means higher need.
Limitation: it treats all concepts the same here, even though inference is harder.

## Inference task
- Evidence: Difficulty_C1, Difficulty_C2, Difficulty_C3, StudentLevel, DaysLeft
- Query: Pr(StudyNeed) and Pr(Stress)
- Algorithm: BeliefPropagation (junction tree from slides)

First test: 
- Struggling student, all hard, exam soon: StudyNeed high = 0.64, Stress high = 0.75
- Advanced student, all easy, exam far away: StudyNeed low = 0.74, Stress low = 0.75

The two students get opposite results, which is what I expected. Stress is exactly 0.75 or 0.25 because it only depends on DaysLeft, which is observed. 

## Utility function: U(StudyNeed, Stress, action)
Score from -10 to 10, made of two parts added together.

Exam success (does the action match how much studying is needed):
- High need: intense +8, practice +3, light 0, rest -6. When I really need to study, the big block helps most and resting hurts.
- Medium need: intense 0, practice +4, light +3, rest -2. Practice fits best, intense is overkill.
- Low need: intense -3, practice -1, light +2, rest +4. I already know it, so heavy studying is wasted time.

Stress:
- High stress: intense -3, practice -1, light 0, rest +2. A big block makes stress worse and resting helps.
- Low stress: no change for any action.

Before settling on these, I tested them on 20 different students to make sure each of the 4 actions gets picked somewhere. My first numbers made practice win almost every time, so I raised intense for high need and lowered practice.

## Expected utility and best action
EU(action) = sum over need and stress of Pr(StudyNeed) * Pr(Stress) * U(StudyNeed, Stress, action)

The system picks the action with the highest EU (MEU principle).

I can multiply Pr(StudyNeed) and Pr(Stress) because they're independent once DaysLeft is observed. Their only shared parent is DaysLeft, and it's always known.

First results:
- Struggling student, all hard, exam soon: intense 2.68, practice 2.28, light 1.01, rest -2.66, so it picks intense
- Advanced student, all easy, exam far away: intense -2.48, practice -0.01, light 2.07, rest 2.69, so it picks rest

For the struggling student, practice was close behind intense (2.28 vs 2.68). That makes sense, since practice is the second most useful action when need is high.

## Calendar
- Uses the Google Calendar API, with login code from Google's Python quickstart
- The system only writes to a separate calendar called "Study Planner", so it never touches my real events
- Before booking, it clears anything it already planned for today, so running it twice doesn't double book
- intense = 5 hours, practice = 2 hours, light = 1 hour, all starting at the next full hour
- rest = clears today and adds an all day "Rest day" event
- Tested by booking a light review session, and it showed up in my calendar

## Main program
main.py connects everything:
- Asks for the exam date and works out days left (3 or less = few)
- Asks if the student is struggling or advanced, and how hard each concept is
- Uses those answers as evidence, runs inference and expected utility, and picks the best action
- Books the action in the Study Planner calendar

Tested:
- Struggling, all hard, exam in 2 days: picked intense, 5 hour block added to the calendar
- Advanced, all easy, exam in 17 days: picked rest, block replaced with a rest day

## Scenarios
I tested 6 students to show the system picks different actions:
- Struggling, all hard, exam soon: intense
- Struggling, all easy, exam soon: practice
- Struggling, all easy, exam far: light
- Advanced, all hard, exam soon: light
- Advanced, only C2 hard, exam soon: light
- Advanced, all easy, exam soon: rest

All 4 actions get picked at least once.

Changing only the concept difficulty changes the action:
- Struggling student with the exam soon: all easy gives practice, all hard gives intense
- Advanced student with the exam soon: all easy gives rest, and making just inference (C2) hard flips it to light

Earlier I was worried student level would matter more than difficulty. The results show difficulty still changes the decision, so I kept my mastery numbers.

The chart is in scenarios.png.

