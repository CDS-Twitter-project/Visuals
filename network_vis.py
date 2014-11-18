import networkx as net
import matplotlib.pyplot as plt

from collections import defaultdict
import math

orig_users = set()
twitter_network = [ line.strip().split('\t') for line in file('twitter_network.csv') ]

o = net.DiGraph()
hfollowers = defaultdict(lambda: 0)
for (twitter_user, followed_by, followers) in twitter_network:
    o.add_edge(twitter_user, followed_by, followers=int(followers))
    hfollowers[twitter_user] = int(followers)
    orig_users.add(twitter_user)

# centre around the SEED node and set radius of graph
g = o

print 'g: ', len(g)
colors = []
d = net.degree(g)
for n in g.nodes():
    if d[n] <= 2:
        g.remove_node(n)
    else:
        if n in orig_users:
            colors.append('red')
        else:
            colors.append('green')

print 'core after node pruning: ', len(g)



plt.figure(figsize=(18,18))
plt.axis('off')

net.draw_networkx(g, node_color=colors)

plt.show()

# nodeset_types = { 'TED': lambda s: s.lower().startswith('ted'), 'Not TED': lambda s: not s.lower().startswith('ted') }

# nodesets = defaultdict(list)

# for nodeset_typename, nodeset_test in nodeset_types.iteritems():
#     nodesets[nodeset_typename] = [ n for n in core.nodes_iter() if nodeset_test(n) ]

# pos = net.spring_layout(core) # compute layout

# colours = ['red','green']
# colourmap = {}

# plt.figure(figsize=(18,18))
# plt.axis('off')

# # draw nodes
# i = 0
# alphas = {'TED': 0.6, 'Not TED': 0.4}
# for k in nodesets.keys():
#     ns = [ math.log10(hfollowers[n]+1) * 80 for n in nodesets[k] ]
#     print k, len(ns)
#     net.draw_networkx_nodes(core, pos, nodelist=nodesets[k], node_size=ns, node_color=colours[i], alpha=alphas[k])
#     colourmap[k] = colours[i]
#     i += 1
# print 'colourmap: ', colourmap

# # draw edges
# net.draw_networkx_edges(core, pos, width=0.5, alpha=0.5)

# # draw labels
# alphas = { 'TED': 1.0, 'Not TED': 0.5}
# for k in nodesets.keys():
#     for n in nodesets[k]:
#         x, y = pos[n]
#         plt.text(x, y+0.02, s=n, alpha=alphas[k], horizontalalignment='center', fontsize=9)

# plt.show()

