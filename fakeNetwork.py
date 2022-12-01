import random
import networkx as nx
from matplotlib import pyplot as plt

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
                attrs[i] = {"id": i, "followers": rand1, "verified": False, "color": "blue"}
                network.add_node(i)
            else:
                attrs[i] = {"id": i, "followers": rand2, "verified": False, "color": "yellow"}
                network.add_node(i)
        else:
            attrs[i] = {"id": i, "followers": rand3, "verified": False, "color": "green"}
            network.add_node(i)
    else:
        attrs[i] = {"id": i, "followers": rand4, "verified": True, "color": "red"}
        network.add_node(i)
nx.set_node_attributes(network, attrs)
p_edge = 0.1
for i in range(network.number_of_nodes()):
    for j in range(i + 1, network.number_of_nodes()):
        if network.nodes[i]["verified"] is True or network.nodes[j]["verified"] is True:
            p_edge = 0.95
        elif network.nodes[i]["followers"] >= 10000 or network.nodes[i]["followers"] >= 10000:
            p_edge = 0.75
        elif 1000 <= network.nodes[i]["followers"] <= 10000 or 1000 <= network.nodes[i]["followers"] <= 10000:
            p_edge = 0.5
        else:
            p_edge = 0.1

        if random.random() < p_edge:
            network.add_edge(i, j)
node_sizes = []
colors = []
centralities = nx.eigenvector_centrality(network)
for i in range(len(centralities)):
    node_sizes.append(centralities[i] * 1000)
    colors.append(network.nodes[i]["color"])

nx.draw(network, node_size=node_sizes, node_color=colors)
plt.show()
