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
