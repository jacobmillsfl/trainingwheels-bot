"""
    Leetcode bot application for the TrainingWheels Discord
"""

import argparse
from dotenv import dotenv_values

from utils.database.database_util import DatabaseUtil
from utils.discord_util import DiscordUtil
from utils.leetcode_util import LeetcodeUtil
from utils.standalone_util import StandaloneUtil


if __name__ == "__main__":
    # Program entry point. Parse arguments and launch relevant initialization routines.

    config = dotenv_values(".process.env")
    DISCORD_AUTH_TOKEN = config.get("DISCORD_AUTH_TOKEN")
    CHANNEL_ID = config.get("CHANNEL_ID")
    database = DatabaseUtil(config.get("DATABASE_NAME"))
    leetcode = LeetcodeUtil()

    command_parser = argparse.ArgumentParser(
        prog="TrainingWheels Bot",
        usage="leetcode_bot.py [--discord] [--update]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
    TrainingWheels Bot.

    A Multi-functional bot built for the TrainingWheels discord server.
    Primary function is to set, track, and record users' LeetCode challenge progress.
    -----------------------------------------
    Default == Standalone version, locally interactable via CLI""",
    )

    command_parser.add_argument(
        "--discord", action="store_true", help="Run the app in Discord mode"
    )

    command_parser.add_argument(
        "--update",
        action="store_true",
        help="Update the database with new Leetcode questions",
    )

    args = command_parser.parse_args()

    if args.update:
        print("Updating Leetcode questions in our database...")
        new_questions = leetcode.api_questions_loadall()
        count = database.leetcode_questions.insert_many(new_questions)
        print(f"Inserted {count} new questions into the database")

    if args.discord:
        print("Running in Discord mode")
        bot = DiscordUtil(
            database=database, token=DISCORD_AUTH_TOKEN, channel_id=CHANNEL_ID, leetcode=leetcode
        )
    else:
        bot = StandaloneUtil(database=database, leetcode=leetcode)

    # Once implemented within discord_util.py & standalone_util.py, enable bot.run()
    bot.run()
