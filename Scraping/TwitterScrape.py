import tweepy
from twitter_authentication import *
import pandas as pd


def add_users(userids, network, visited):
    for i in userids:
        if (i not in visited) and (network[i][1] > 0):
            follower_names = client.get_users_followers(id=i, user_fields='public_metrics', max_results=10)
            visited[i] = True
            for user in follower_names.data:
                network[i][2].append(user.id)
                network[user.id] = (user.username, user.public_metrics['followers_count'], [])


def ids_generator(network, visited):
    ids = []
    for i in network:
        ids.append(i)
    add_users(ids, network, visited)


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
add_users([elon_id], network, visited)
ids_generator(network, visited)

print(network)
