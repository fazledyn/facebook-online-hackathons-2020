import praw
import requests
from PIL import Image
from io import BytesIO

from datetime import datetime
from .models import Meme, Joke, Pun

from .config import CLIENT_ID, CLIENT_SECRET, USER_AGENT, USERNAME, PASSWORD, MEME_COUNT, JOKE_COUNT, PUN_COUNT

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     username=USERNAME,
                     password=PASSWORD
                     )


def fetch_meme():
    meme_sub = reddit.subreddit('meme')
    memes_sub = reddit.subreddit('memes')
    memeeconomy_sub = reddit.subreddit('MemeEconomy')
    darkmemes_sub = reddit.subreddit('DarkMemesForDarkHumou')

    subs = [meme_sub, memes_sub, memeeconomy_sub, darkmemes_sub]

    count = 0
    for sub in subs:
        for item in sub.new(limit=MEME_COUNT):
            if not item.over_18:
                Meme.objects.create(
                    title=item.title, url=item.url, source=item.subreddit)
                count += 1

    print("[In fetch_meme()]: New items crawled: ", count)
    return count


def fetch_joke():
    joke_sub = reddit.subreddit('Jokes')

    count = 0
    for item in joke_sub.new(limit=JOKE_COUNT):
        if not item.over_18:
            Joke.objects.create(title=item.title, content=item.selftext)
            count += 1

    print("[In fetch_joke()]: New items crawled: ", count)
    return count


def fetch_pun():
    pun_sub1 = reddit.subreddit('puns')
    pun_sub2 = reddit.subreddit('Punny')
    pun_sub_list = [pun_sub1, pun_sub2]

    count = 0
    for sub in pun_sub_list:
        for item in sub.new(limit=PUN_COUNT):
            Pun.objects.create(
                title=item.title, content=item.selftext, url=item.url)
            count += 1

    print("[In fetch_pun()]: New items crawled: ", count)
    return count


if __name__ == "__main__":
    fetch_meme()
    fetch_joke()
    fetch_pun()
