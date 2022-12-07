# from collections import Counter
# import matplotlib.pyplot as plt
# import networkx as nx
# import numpy as np
# from numpy.ma import log10
#
#
# def drop_zeros(a_list):
#     return [i for i in a_list if i > 0]
#
#
# def log_binning(counter_dict, bin_count=35):
#     cdk = list(counter_dict.keys())
#     cdv = list(counter_dict.values())
#     max_x = log10(max(cdk))
#     max_y = log10(max(cdv))
#     max_base = max([max_x, max_y])
#     min_x = log10(min(drop_zeros(cdk)))
#     bins = np.logspace(min_x, max_base, num=bin_count)
#     bin_means_y = (np.histogram(cdk, bins, weights=cdv)[0] / np.histogram(cdk, bins)[0])
#     bin_means_x = (np.histogram(cdk, bins, weights=cdk)[0] / np.histogram(cdk, bins)[0])
#
#     return bin_means_x, bin_means_y
#
#
# def plot(graph, name):
#     c = nx.degree_centrality(graph)
#     c2 = dict(Counter(c.values()))
#     x, y = log_binning(c2, 50)
#     plt.xscale('log')
#     plt.yscale('log')
#     plt.scatter(x, y, c='r', marker='s', s=50)
#     plt.scatter(c2.keys(), c2.values(), c='b', marker='x')
#     plt.xlim((1e-3, 1))
#     plt.ylim((0.5, 1e3))
#     plt.title(name)
#     plt.xlabel('Connections (normalized)')
#     plt.ylabel('Frequency')
#     plt.show()
#
#
# dejan = nx.read_gml("Scraping/Dejan-Full-Node-Info.gml")
# plot(dejan, "Dejan Network")
#
# # ba = nx.barabasi_albert_graph(1000, 4, 1)
# # plot(ba, "Barabasi Albert Graph")
