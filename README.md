# Bayesian Study Planner

COSC 329 Learning Analytics, final project (Option 3)
Gulsher Assad

This is a study planner that decides how you should study today before an exam. It uses a Bayesian network to estimate how much you need to study and how stressed you probably are, then picks the action with the highest expected utility and books it in Google Calendar.

The four actions are:
- intense: 5 hour study block
- practice: 2 hour practice problem session
- light: 1 hour review session
- rest: clear the day and take a rest day

The network models three concepts from this course:
- C1: Bayes' rule
- C2: Bayes net inference
- C3: Expected utility

## Files

- `planner_bn.py` builds the Bayes net (10 variables) and all the CPTs. Running it checks the model, runs two test queries and draws the network.
- `decision.py` has the four actions, the utility function and the expected utility calculation. Running it shows the decision for a struggling and an advanced student.
- `calendar_api.py` handles logging into Google Calendar and booking the chosen action. Running it books a test light review session.
- `main.py` is the full program. You type in your exam date and info, and it picks the best action and books it.
- `scenarios.py` tests six different students and saves a chart of the results to `scenarios.png`.
- `design.md` explains all my design choices: the variables, arrows, every CPT and why I picked the numbers, the utility function and the results.
- `network.png` is a picture of the network.
- `scenarios.png` is the results chart.

## Setup

You need Python 3.

1. Clone the repo and go into the folder.
2. Make a virtual environment and install the libraries:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

The Bayes net, the decision part and the scenarios work without any Google setup. Only `calendar_api.py` and `main.py` need the steps below.

## Google Calendar setup

1. Go to console.cloud.google.com and make a new project.
2. Search for Google Calendar API and enable it.
3. Set up the OAuth consent screen. Choose External, and add your own Gmail under Test users (login won't work without this).
4. Under Clients, create an OAuth client ID with the type Desktop app.
5. Download the JSON file, rename it to `credentials.json` and put it in the project folder.

The first time you run something that uses the calendar, a browser window opens to log in. Google will say the app isn't verified. That's normal for a personal project, so just click Continue. After that it saves a `token.json` file so you don't have to log in again.

`credentials.json` and `token.json` are in `.gitignore` and should never be committed.

The planner only writes to its own calendar called "Study Planner", which it creates the first time. It never touches your other events.

## Running the planner

```
python main.py
```

It asks for:
- your exam dates (YYYY-MM-DD, separate with commas). It plans for the closest one.
- whether you're struggling or advanced
- whether each concept is easy or hard for you

Type each answer and press Enter. Use lowercase exactly as shown.

It then goes through every day until the exam, picks the best action for each day, and books it in your Study Planner calendar. Today's session starts at the next full hour, and other days start at 10am. Running it again replaces what it booked before.

Example: a struggling student who finds all three concepts hard, with the exam 6 days away, gets practice sessions for the first 3 days and intense 5 hour blocks for the last 3 days.

## Other things you can run

```
python planner_bn.py   # check the model and see the network
python decision.py     # see the decision for two example students
python scenarios.py    # test six students and save the results chart
```

## How it works

1. The inputs (student level, how hard each concept is, days until the exam) are set as evidence in the Bayes net.
2. Belief propagation infers two things: how much studying is needed (StudyNeed) and how stressed the student is (Stress).
3. The utility function scores each action from -10 to +10, based on exam success and stress.
4. Expected utility is worked out for each action, and the one with the highest EU is picked.
5. This is repeated for every day until the exam, and each day's action is booked in Google Calendar.

All the details and the reasoning behind every number are in `design.md`.

## Limitations

- Answers have to be typed exactly (for example `hard`, not `Hard`), or the program crashes.
- Stress only depends on how many days are left.
- Mastery doesn't go up after studying, so the model doesn't learn over time. A dynamic Bayes net would be the way to add that.
- All variables are simple (two or three values), and the CPTs are handcrafted, not learned from data.
- The plan only changes when the exam gets within 3 days, because mastery doesn't go up after studying.
- Google logins expire after 7 days while the app is in testing mode. If you get an "invalid_grant" error, delete token.json and run again.
