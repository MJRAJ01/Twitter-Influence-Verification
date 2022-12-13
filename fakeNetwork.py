import random
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from numpy.ma import log10


# Generates an artificial network
def fake_network():
    network = nx.DiGraph()
    attrs = {}
    for i in range(1000):
        # Creating groups of follower ranges
        rand1 = random.randint(10, 1000)
        rand2 = random.randint(1000, 10000)
        rand3 = random.randint(10000, 50000)
        rand4 = random.randint(50000, 1000000)
        p_followers = .95
        # More likely to draw smaller range
        if random.random() < p_followers:
            if random.random() < p_followers:
                if random.random() < p_followers:
                    attrs[i] = {"id": i, "followers": rand1}
                    network.add_node(i)
                else:
                    attrs[i] = {"id": i, "followers": rand2}
                    network.add_node(i)
            else:
                attrs[i] = {"id": i, "followers": rand3}
                network.add_node(i)
        else:
            attrs[i] = {"id": i, "followers": rand4}
            network.add_node(i)
        # More likely to be verified with more followers
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
    # More likely to have connections with greater follower counts
    for i in range(network.number_of_nodes()):
        for j in range(network.number_of_nodes()):
            if network.nodes[i]["followers"] >= 50000 and network.nodes[j]["followers"] >= 50000:
                p_edge = 0.25
                if random.random() < p_edge \
                        and len(network.in_edges(i)) < network.nodes[i]["followers"] \
                        and len(network.in_edges(j)) < network.nodes[j]["followers"]:
                    network.add_edge(j, i)
                    network.add_edge(i, j)
            elif network.nodes[i]["followers"] >= 50000 and network.nodes[j]["followers"] >= 10000:
                p_edge = 0.15
                if random.random() < p_edge \
                        and len(network.in_edges(i)) < network.nodes[i]["followers"] \
                        and len(network.in_edges(j)) < network.nodes[j]["followers"]:
                    network.add_edge(j, i)
                    network.add_edge(i, j)
            elif network.nodes[i]["followers"] >= 10000 and network.nodes[j]["followers"] >= 10000:
                p_edge = 0.1
                if random.random() < p_edge \
                        and len(network.in_edges(i)) < network.nodes[i]["followers"] \
                        and len(network.in_edges(j)) < network.nodes[j]["followers"]:
                    network.add_edge(j, i)
                    network.add_edge(i, j)
            else:
                if network.nodes[i]["followers"] >= 50000:
                    p_edge = 0.05
                elif network.nodes[i]["followers"] >= 10000:
                    p_edge = 0.025
                elif network.nodes[i]["followers"] >= 1000:
                    p_edge = 0.01
                else:
                    p_edge = 0.005

                if random.random() < p_edge \
                        and len(network.in_edges(i)) < network.nodes[i]["followers"]:
                    network.add_edge(j, i)
    return network


def drop_zeros(a_list):
    return [i for i in a_list if i > 0]


def log_binning(counter_dict, bin_count=35):
    cdk = list(counter_dict.keys())
    cdv = list(counter_dict.values())
    max_x = log10(max(cdk))
    max_y = log10(max(cdv))
    max_base = max([max_x, max_y])
    min_x = log10(min(drop_zeros(cdk)))
    bins = np.logspace(min_x, max_base, num=bin_count)
    bin_means_y = (np.histogram(cdk, bins, weights=cdv)[0] / np.histogram(cdk, bins)[0])
    bin_means_x = (np.histogram(cdk, bins, weights=cdk)[0] / np.histogram(cdk, bins)[0])

    return bin_means_x, bin_means_y


def plot(graph, name):
    c = nx.degree_centrality(graph)
    c2 = dict(Counter(c.values()))
    x, y = log_binning(c2, 50)
    plt.xscale('log')
    plt.yscale('log')
    plt.scatter(x, y, c='r', marker='s', s=50)
    plt.scatter(c2.keys(), c2.values(), c='b', marker='x')
    plt.xlim((1e-3, 1))
    plt.ylim((0.5, 1e3))
    plt.title(name)
    plt.xlabel('Connections (normalized)')
    plt.ylabel('Frequency')
    plt.show()


# Plotting connections normalized with frequencies of each network
dejan = nx.read_gml("Scraping/Dejan-Full-Node-Info.gml")
plot(dejan, "Dejan Network")

artificial = fake_network()
nx.write_gml(artificial, "fakeNetwork.gml")

plot(artificial, "Artificial Network")

hedden = nx.read_gml("Scraping/Hedden.gml")
plot(hedden, "Hedden")

mccormick = nx.read_gml("Scraping/McCormick.gml")
plot(mccormick, "McCormick")

# Collecting stats of each network (number of nodes, avg path length, avg clustering, largest component, average degree)
stats = {"hedden": {}, "dejan": {}, "mccormick": {}, "artificial": {}}

stats["hedden"]["n"] = nx.number_of_nodes(hedden)
stats["dejan"]["n"] = nx.number_of_nodes(dejan)
stats["mccormick"]["n"] = nx.number_of_nodes(mccormick)
stats["artificial"]["n"] = nx.number_of_nodes(artificial)

stats["hedden"]["Avg. Path Length"] = nx.average_shortest_path_length(hedden)
stats["dejan"]["Avg. Path Length"] = nx.average_shortest_path_length(dejan)
stats["mccormick"]["Avg. Path Length"] = nx.average_shortest_path_length(mccormick)
stats["artificial"]["Avg. Path Length"] = nx.average_shortest_path_length(artificial)

stats["hedden"]["Avg. Clustering"] = nx.average_clustering(hedden)
stats["dejan"]["Avg. Clustering"] = nx.average_clustering(dejan)
stats["mccormick"]["Avg. Clustering"] = nx.average_clustering(mccormick)
stats["artificial"]["Avg. Clustering"] = nx.average_clustering(artificial)

hedden_largest_component = max(nx.strongly_connected_components(hedden), key=len)
dejan_largest_component = max(nx.strongly_connected_components(dejan), key=len)
mccormick_largest_component = max(nx.strongly_connected_components(mccormick), key=len)
artificial_largest_component = max(nx.strongly_connected_components(artificial), key=len)
stats["hedden"]["Largest Component"] = 100 * len(hedden_largest_component) / nx.number_of_nodes(hedden)
stats["dejan"]["Largest Component"] = 100 * len(dejan_largest_component) / nx.number_of_nodes(dejan)
stats["mccormick"]["Largest Component"] = 100 * len(mccormick_largest_component) / nx.number_of_nodes(mccormick)
stats["artificial"]["Largest Component"] = 100 * len(artificial_largest_component) / nx.number_of_nodes(artificial)

hedden_degree = 0
dejan_degree = 0
mccormick_degree = 0
artificial_degree = 0
for node in hedden.nodes():
    hedden_degree += hedden.degree[node]
for node in dejan.nodes():
    dejan_degree += dejan.degree[node]
for node in mccormick.nodes():
    mccormick_degree += mccormick.degree[node]
for node in artificial.nodes():
    artificial_degree += artificial.degree[node]
hedden_degree /= nx.number_of_nodes(hedden)
dejan_degree /= nx.number_of_nodes(dejan)
mccormick_degree /= nx.number_of_nodes(mccormick)
artificial_degree /= nx.number_of_nodes(artificial)
stats["hedden"]["Avg. Degree"] = hedden_degree
stats["dejan"]["Avg. Degree"] = dejan_degree
stats["mccormick"]["Avg. Degree"] = mccormick_degree
stats["artificial"]["Avg. Degree"] = artificial_degree

for i in stats:
    print(f'{i}:\n')
    for j in stats[i]:
        if j == "Largest Component":
            print(f'{j}: {round(stats[i][j], 2)}%')
        else:
            print(f'{j}: {round(stats[i][j], 2)}')
    print()
