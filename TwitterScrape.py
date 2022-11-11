import tweepy
from twitter_authentication import *
import pandas as pd

client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret,
                       wait_on_rate_limit=True)

network = {}
visited = {}
elon = client.get_user(id=44196397, user_fields='public_metrics')
elon_username = elon.data.username
elon_follower_count = elon.data.public_metrics['followers_count']
elon_id = elon.data.id
elon_followers = []
network[elon_id] = (elon_username, elon_follower_count, elon_followers)
print(network)
follower_names = client.get_users_followers(id=44196397, user_fields='public_metrics', max_results=10)
visited[elon_id] = True
for user in follower_names.data:
    network[elon_id][2].append(user.id)
    network[user.id] = (user.username, user.public_metrics['followers_count'], [])
print(network)
