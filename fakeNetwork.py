import random
import networkx as nx
from matplotlib import pyplot as plt


# def readFromFile(filename, graph):
#     file = open(filename, "r")
#     ids = {}
#     real_attrs = {}
#     while True:
#         line = file.readline()
#         if line.startswith(","):
#             continue
#         if not line:
#             break
#
#         vals = line.split(",")
#         userid = int(vals[2])
#         follower = int(float(vals[3]))
#         followerCount = int(float(vals[4]))
#         if ids.get(follower) is None:
#             ids[follower] = False
#         if ids.get(userid) is None:
#             if ids.get(userid + 1) is not None:
#                 userid += 1
#             elif ids.get(userid - 1) is not None:
#                 userid -= 1
#         ids[userid] = True
#
#         graph.add_edge(userid, follower)
#         real_attrs[userid] = {"id": userid, "followers": followerCount}
#         if str(vals[5]) == "True":
#             real_attrs[userid]["verified"] = True
#         else:
#             real_attrs[userid]["verified"] = False
#
#         # Default data for users we haven't gathered data on
#         p = 0.998
#         if ids[follower] == False:
#             if random.random() < p:
#                 real_attrs[follower] = {"id": follower, "followers": 700, "verified": False}
#             else:
#                 real_attrs[follower] = {"id": follower, "followers": 50000, "verified": True}
#     count = 0
#     for i in real_attrs:
#         if real_attrs[i]["followers"] != 700 and real_attrs[i]["followers"] != 50000:
#             print(real_attrs[i]["followers"])
#             count += 1
#     print(f"Count: {count}")
#     return real_attrs

def fake_network():
    network = nx.Graph()
    attrs = {}
    for i in range(1000):
        rand1 = random.randint(10, 1000)
        rand2 = random.randint(1000, 10000)
        rand3 = random.randint(10000, 50000)
        rand4 = random.randint(50000, 1000000)
        p_followers = .95
        if random.random() < p_followers:
            if random.random() < p_followers:
                if random.random() < p_followers:
                    attrs[i] = {"id": i, "followers": rand1, "color": "green"}
                    network.add_node(i)
                else:
                    attrs[i] = {"id": i, "followers": rand2, "color": "yellow"}
                    network.add_node(i)
            else:
                attrs[i] = {"id": i, "followers": rand3, "color": "orange"}
                network.add_node(i)
        else:
            attrs[i] = {"id": i, "followers": rand4, "color": "red"}
            network.add_node(i)
        if attrs[i]["followers"] < 42000:
            if random.random() < 0.998:
                attrs[i]["verified"] = False
            else:
                attrs[i]["verified"] = True
        else:
            if random.random() < 0.50:
                attrs[i]["verified"] = False
            else:
                attrs[i]["verified"] = True
    nx.set_node_attributes(network, attrs)
    p_edge = 0.1
    for i in range(network.number_of_nodes()):
        for j in range(i + 1, network.number_of_nodes()):
            if network.nodes[i]["followers"] >= 50000 or network.nodes[i]["followers"] >= 50000:
                p_edge = 0.25
            elif network.nodes[i]["followers"] >= 10000 or network.nodes[i]["followers"] >= 10000:
                p_edge = 0.1
            elif network.nodes[i]["followers"] >= 1000 or network.nodes[i]["followers"] >= 1000:
                p_edge = 0.05
            else:
                p_edge = 0.025

            if random.random() < p_edge \
                    and len(network.edges(i)) < network.nodes[i]["followers"] \
                    and len(network.edges(j)) < network.nodes[j]["followers"]:
                network.add_edge(i, j)
    return network


network = fake_network()
node_sizes = []
colors = []
# if we switch to directed graph we should use katz or pagerank
centralities = nx.eigenvector_centrality(network)
for i in range(len(centralities)):
    node_sizes.append(centralities[i] * 100)
    colors.append(network.nodes[i]["color"])
nx.draw(network, node_size=node_sizes, node_color=colors, width=0.025)
plt.show()

# real = nx.Graph()
# real_attrs = readFromFile("hedden_network_with_followers_verified.csv", real)
nx.write_gexf(network, 'fakeNetwork.gexf')
