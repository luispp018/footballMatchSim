from flask import Flask, render_template, request, redirect, url_for
from random import randint

app = Flask(__name__)

# Function to check if the penalty shootout is still open for grabs
def is_shootout_open_for_grabs(goals_a, goals_b, remaining_kicks):
    return abs(goals_a - goals_b) <= remaining_kicks

# Extra time and penalties function
def extra_time_penalties(t1_goals, t2_goals, team1, team2):
    events = []
    events.append("It's a draw. We go to extra time!")
    chance_counter = 1

    while chance_counter < 4:
        chance_goal_1 = randint(1, 100)
        chance_goal_2 = randint(1, 100)

        time_goal_1 = randint(chance_counter * 10 - 10 + 90, chance_counter * 10 - 1 + 90)
        time_goal_2 = randint(time_goal_1, chance_counter * 10 - 1 + 90)

        if chance_goal_1 > 95:
            t1_goals += 1
            events.append(f"GOAL! {team1} ({t1_goals}-{t2_goals}) {time_goal_1} min")

        if chance_goal_2 > 95:
            t2_goals += 1
            events.append(f"GOAL! {team2} ({t1_goals}-{t2_goals}) {time_goal_2} min")

        chance_counter += 1

    events.append(f"FINAL SCORE AET: {team1} {t1_goals} - {t2_goals} {team2}")

    if t1_goals == t2_goals:
        events.append("It's a draw. We go to penalties!")
        t1_penalties = 0
        t2_penalties = 0
        penalty_counter = 1
        remaining_kicks = 5

        while penalty_counter <= 5 and is_shootout_open_for_grabs(t1_penalties, t2_penalties, remaining_kicks):
            penalty1 = randint(1, 10)
            penalty2 = randint(1, 10)

            if penalty1 > 3:
                t1_penalties += 1
                events.append(f"GOAL! {team1} ({t1_penalties}-{t2_penalties})")
            else:
                events.append(f"MISS! {team1} ({t1_penalties}-{t2_penalties})")

            if penalty2 > 3:
                t2_penalties += 1
                events.append(f"GOAL! {team2} ({t1_penalties}-{t2_penalties})")
            else:
                events.append(f"MISS! {team2} ({t1_penalties}-{t2_penalties})")

            penalty_counter += 1
            remaining_kicks -= 1

        if t1_penalties == t2_penalties:
            while t1_penalties == t2_penalties:
                penalty1 = randint(1, 10)
                penalty2 = randint(1, 10)

                if penalty1 > 3:
                    t1_penalties += 1
                    events.append(f"GOAL! {team1} ({t1_penalties}-{t2_penalties})")
                else:
                    events.append(f"MISS! {team1} ({t1_penalties}-{t2_penalties})")

                if penalty2 > 3:
                    t2_penalties += 1
                    events.append(f"GOAL! {team2} ({t1_penalties}-{t2_penalties})")
                else:
                    events.append(f"MISS! {team2} ({t1_penalties}-{t2_penalties})")

        events.append(f"FINAL SCORE PENALTIES: {team1} {t1_penalties} - {t2_penalties} {team2}")
        if t1_penalties > t2_penalties:
            events.append(f"{team1} wins on penalties!")
        else:
            events.append(f"{team2} wins on penalties!")

    return events

# Regular match generator function
def regular_match(team1, team2, odds):
    events = []
    t1_goals = 0
    t2_goals = 0
    reverse_odds = 100 - odds
    chance_counter = 1

    while chance_counter <= 10:
        chance_goal_1 = randint(odds, 100)
        chance_goal_2 = randint(reverse_odds, 100)

        if chance_counter == 10:
            time_goal_1 = randint(chance_counter * 10 - 10, chance_counter * 10 - 4)
            time_goal_2 = randint(time_goal_1, chance_counter * 10 - 4)
        else:
            time_goal_1 = randint(chance_counter * 10 - 10, chance_counter * 10 - 1)
            time_goal_2 = randint(time_goal_1, chance_counter * 10 - 1)

        if chance_goal_1 > 95:
            t1_goals += 1
            events.append(f"GOAL! {team1} ({t1_goals}-{t2_goals}) {time_goal_1} min")

        if chance_goal_2 > 95:
            t2_goals += 1
            events.append(f"GOAL! {team2} ({t1_goals}-{t2_goals}) {time_goal_2} min")

        chance_counter += 1

    events.append(f"FINAL SCORE: {team1} {t1_goals} - {t2_goals} {team2}")

    if t1_goals == t2_goals:
        events.extend(extra_time_penalties(t1_goals, t2_goals, team1, team2))

    return events

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        odds = int(request.form['odds'])
        match_type = request.form['match_type']

        if match_type == 'regular':
            events = regular_match(team1, team2, odds)
        else:
            events = extra_time_penalties(0, 0, team1, team2)

        return render_template('index.html', events=events, team1=team1, team2=team2)

    return render_template('index.html', events=None)

if __name__ == '__main__':
    app.run(debug=True)