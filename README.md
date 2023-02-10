# trainingwheels-bot
Discord bot for the Training Wheels server


## Getting started

First, create a Python virtual environment named `bot-env`
```
python3 -m venv bot-env
```

Next, activate the Python virtual environment
```
source bot-env/bin/activate
```

It is important that you do the command above before continuing. Once inside virtual environment, install dependencies.

```
python3 -m pip install -r requirements.txt
```

When you are finished, if you wish to continue using the terminal for different projects, you should deactivate the Python virtual environment.
```
deactivate
```

Now you can use your shell as normal, just re-activate the virtual environment whenever you want to run this project's code again.

## Testing leetcode API access
Make sure you are running in a Python virtual environment before running any of the project code.
You can test interacting with leetcode using the following command, which runs the `leetcode-questions.py` script.
```
python3 leetcode-questions.py
```

## E/R Diagram for Database

![E/R Diagram](./assets/bot_er_diagram.png "Optional title")

`Leetcode_Question` contains all leetcode questions, scraped once at the launch of the app/db.

`Leetcode_User` maps a DiscordID to a Leetcode ID. We would want this for stuff like !leetcode stats or !leetcode rank commands.

`Leetcode_WeeklyChallenge` is the challenge we create each week. It is simple a date and a uniq identifier for "Week 1", "Week 2", etc.

`Leetcode_WeeklyQuestion` is a collection of questions associated with a Leetcode_WeeklyChallenge.