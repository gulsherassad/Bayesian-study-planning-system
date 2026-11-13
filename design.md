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