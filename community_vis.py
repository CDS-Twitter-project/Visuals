import networkx as net
import matplotlib.pyplot as plt

from collections import defaultdict
import math
import communities

orig_users = set()
twitter_network = [ line.strip().split('\t') for line in file('twitter_network.csv') ]

o = net.DiGraph()
hfollowers = defaultdict(lambda: 0)
for (twitter_user, followed_by, followers) in twitter_network:
    o.add_edge(twitter_user, followed_by, followers=int(followers))
    hfollowers[twitter_user] = int(followers)
    orig_users.add(twitter_user)

g = o

print 'g: ', len(g)
d = net.degree(g)
for n in g.nodes():
    if d[n] <= 2:
        g.remove_node(n)

print 'core after node pruning: ', len(g)

comm = communities.GirvanNewman(g.to_undirected())

gr2 = comm.communities(10)

net.draw_networkx(gr2)
plt.axis('off')
plt.show()