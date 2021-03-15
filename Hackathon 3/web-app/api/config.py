import os
from hackathon.settings import SECRET_KEY


""" Facebook Api/Bot VARS """
ACCESS_TOKEN = "EAAUGlfzWZCLABALDOhSbSnLomZA4hYvf4dfoNNwRL9QYNrYugZAxWtWfgE91SMETdnbEnsG4jjA95QUqYfBQiaUUkHZAFgrdzVHvvOZAypYKJtZAiR1ZCiDJYuKcrtY7lmJXhCr03tK0BZAUkXfTBvWutax5K2ZC2morrmtQWFXOTfrYA84S5aLI3"
API_VERSION = "7.0"


""" Reddit VARS """
MEME_COUNT = 10
JOKE_COUNT = 5
PUN_COUNT = 5


# Reddit API Login
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

USER_AGENT = os.environ.get("USER_AGENT")
USERNAME = os.environ.get("REDDIT_USERNAME")
PASSWORD = os.environ.get("REDDIT_PASSWORD")


""" Custom VAR """
# In seconds
JOB_TIME_INTERVAL = 86400
FETCH_TOKEN = "whoopwhoop"
SEQUENCE_RATIO = 0.5
