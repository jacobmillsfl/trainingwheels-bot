"""
    Leetcode bot application for the TrainingWheels Discord
"""
from dotenv import dotenv_values

from utils.database_util import DatabaseUtil
#from utils.discord_util import DiscordUtil
from utils.leetcode_util import LeetcodeUtil
#from utils.standalone_util import StandaloneUtil




if __name__ == "__main__":
    # Program entry point. Parse arguments and launch relevant initialization routines.


    config = dotenv_values("../.process.env")

    #Note: this is currently a dummy token. Update with official discord bot token once registered.
    DISCORD_AUTH_TOKEN = config.get("DISCORD_AUTH_TOKEN")

    # Example of how to pull all leetcode questions and enter into the database
    # This will eventually be part of our app initialization routine
    new_questions = LeetcodeUtil.api_questions_loadall()
    database = DatabaseUtil(config.get("DATABASE_NAME"))
    count = database.table_leetcodequestion_insert_many(new_questions)
    print(f"Inserted {count} new questions into the database")


    # Warning: this is just for debugging and will print a lot of data
    #           if it does, then it worked
    #our_questions = database.table_leetcodequestion_loadall()
    #print(our_questions)


    # Note: Implement argparse to parse `--discord` argument if set.
    #       After parsing arguments, we will do something like the following:
    #
    # if "discord mode":
    #     bot = DiscordUtil(DISCORD_AUTH_TOKEN)
    # else:
    #     bot = StandaloneUtil()
    #
    #bot.run()
