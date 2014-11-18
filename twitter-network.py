import glob
import os
import json
import sys
from collections import defaultdict

users = defaultdict(lambda: { 'followers': 0 })

for f in glob.glob('twitter-users/*.json'):
    data = json.load(file(f))
    screen_name = data['screen_name']
    users[screen_name] = { 'followers': data['followers_count'] }


def process_follower_list(screen_name, edges=[]):
    f = os.path.join('followers_data', screen_name + '.csv')

    if not os.path.exists(f):
        return edges

    followers = [line.strip().split('\t') for line in file(f)]

    for follower_data in followers:
        if len(follower_data) < 2:
            continue

        screen_name_2 = follower_data[1]

        # use the number of followers for screen_name as the weight
        weight = users[screen_name]['followers']

        edges.append([screen_name, screen_name_2, weight])

        #process_follower_list(screen_name_2, edges)

    return edges
edges = []

for user in users:
    edges += process_follower_list(user)

with open('twitter_network.csv', 'w') as outf:
    edge_exists = {}
    for edge in edges:
        key = ','.join([str(x) for x in edge])
        if not(key in edge_exists):
            outf.write('%s\t%s\t%d\n' % (edge[0], edge[1], edge[2]))
            edge_exists[key] = True
