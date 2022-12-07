import random
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from numpy.ma import log10


def fake_network():
    network = nx.DiGraph()
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
        # if attrs[i]["followers"] < 42000:
        #     if random.random() < 0.5:
        #         attrs[i]["verified"] = False
        #     else:
        #         attrs[i]["verified"] = True
        # else:
        if random.random() < 0.50:
            attrs[i]["verified"] = False
        else:
            attrs[i]["verified"] = True
    nx.set_node_attributes(network, attrs)
    p_edge = 0.1
    for i in range(network.number_of_nodes()):
        for j in range(network.number_of_nodes()):
            if network.nodes[i]["followers"] >= 50000 and network.nodes[j]["followers"] >= 50000:
                p_edge = 0.5
                if random.random() < p_edge \
                        and len(network.in_edges(i)) < network.nodes[i]["followers"] \
                        and len(network.in_edges(j)) < network.nodes[j]["followers"]:
                    network.add_edge(j, i)
                    network.add_edge(i, j)
            elif network.nodes[i]["followers"] >= 50000 and network.nodes[j]["followers"] >= 10000:
                p_edge = 0.25
                if random.random() < p_edge \
                        and len(network.in_edges(i)) < network.nodes[i]["followers"] \
                        and len(network.in_edges(j)) < network.nodes[j]["followers"]:
                    network.add_edge(j, i)
                    network.add_edge(i, j)
            elif network.nodes[i]["followers"] >= 10000 and network.nodes[j]["followers"] >= 10000:
                p_edge = 0.2
                if random.random() < p_edge \
                        and len(network.in_edges(i)) < network.nodes[i]["followers"] \
                        and len(network.in_edges(j)) < network.nodes[j]["followers"]:
                    network.add_edge(j, i)
                    network.add_edge(i, j)
            else:
                if network.nodes[i]["followers"] >= 50000:
                    p_edge = 0.15
                elif network.nodes[i]["followers"] >= 10000:
                    p_edge = 0.075
                elif network.nodes[i]["followers"] >= 1000:
                    p_edge = 0.025
                else:
                    p_edge = 0.01

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


dejan = nx.read_gml("Scraping/Dejan-Full-Node-Info.gml")
plot(dejan, "Dejan Network")

network = fake_network()
nx.write_gml(network, "fakeNetwork.gml")
# node_sizes = []
# colors = []
# # if we switch to directed graph we should use katz or pagerank
# centralities = nx.pagerank(network)
# for i in range(len(centralities)):
#     node_sizes.append(centralities[i] * 10000)
#     colors.append(network.nodes[i]["color"])
# nx.draw(network, node_size=node_sizes, node_color=colors, width=0.025, arrowsize=0.01)
# plt.show()
#
# plot(network, "Artificial Network")

hedden = nx.read_gml("Scraping/Hedden.gml")
plot(hedden, "Hedden")

mccormick = nx.read_gml("Scraping/McCormick.gml")
plot(mccormick, "McCormick")
