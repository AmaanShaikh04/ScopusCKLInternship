# File name: author.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
from networkx.algorithms.community import greedy_modularity_communities

FILE_PATH = "285scopus_wearables_ai_education_corpus.csv"
AUTHOR_COLUMN = "Authors"

df = pd.read_csv(FILE_PATH)

author_counts = Counter()

for authors in df[AUTHOR_COLUMN].dropna():
    for author in authors.split(";"):
        author_counts[author.strip()] += 1

def build_author_graph(min_pubs):
    G = nx.Graph()

    for authors in df[AUTHOR_COLUMN].dropna():
        author_list = [
            a.strip() for a in authors.split(";")
            if a.strip() and author_counts[a.strip()] >= min_pubs
        ]

        for author in author_list:
            G.add_node(author)

        for a1, a2 in combinations(author_list, 2):
            if G.has_edge(a1, a2):
                G[a1][a2]["weight"] += 1
            else:
                G.add_edge(a1, a2, weight=1)

    return G

def visualize_graph(G, title, node_scale=20, label_size=7):
    if G.number_of_nodes() == 0:
        print(f"No authors found for {title}")
        return

    communities = list(greedy_modularity_communities(G))
    author_cluster = {}

    for i, comm in enumerate(communities):
        for author in comm:
            author_cluster[author] = i

    pos = nx.spring_layout(G, k=0.18, seed=42)

    node_colors = [author_cluster.get(n, 0) for n in G.nodes()]
    node_sizes = [(G.degree(n) + 1) * node_scale for n in G.nodes()]

    plt.figure(figsize=(24, 24))

    nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.5)
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=plt.cm.tab20,
        alpha=0.9
    )
    nx.draw_networkx_labels(G, pos, font_size=label_size)

    plt.title(title, fontsize=18)
    plt.axis("off")
    plt.show()

for min_pubs in [1, 2, 3]:
    print(f"\n=== Minimum publications: {min_pubs} ===")

    G = build_author_graph(min_pubs)

    print(f"Authors: {G.number_of_nodes()}")
    print(f"Co-author links: {G.number_of_edges()}")

    visualize_graph(
        G,
        title=f"Author Network (All Authors, Minimum Publications ≥ {min_pubs})",
        node_scale=30,
        label_size=7
    )

    if G.number_of_nodes() > 0:
        largest_cc = max(nx.connected_components(G), key=len)
        G_largest = G.subgraph(largest_cc).copy()

        visualize_graph(
            G_largest,
            title=(
                "Author Network (Largest Connected Component, "
                f"Minimum Publications ≥ {min_pubs})"
            ),
            node_scale=40,
            label_size=8
        )
