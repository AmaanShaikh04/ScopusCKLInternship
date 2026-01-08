# File name: organization.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
from networkx.algorithms.community import greedy_modularity_communities

FILE_PATH = "285scopus_wearables_ai_education_corpus.csv"
AFFILIATION_COLUMN = "Affiliations"

df = pd.read_csv(FILE_PATH)

paper_orgs = []
org_publication_count = Counter()

for aff in df[AFFILIATION_COLUMN].dropna():
    orgs = [o.strip() for o in aff.split(";") if len(o.strip()) > 3]
    unique_orgs = list(set(orgs))

    paper_orgs.append(unique_orgs)

    for org in unique_orgs:
        org_publication_count[org] += 1

print(f"Total unique organizations: {len(org_publication_count)}")

def build_and_plot_org_network(min_pubs):
    print(f"\n=== Organization Network | Min publications ≥ {min_pubs} ===")

    valid_orgs = {o for o, c in org_publication_count.items() if c >= min_pubs}

    G = nx.Graph()

    for orgs in paper_orgs:
        filtered = [o for o in orgs if o in valid_orgs]

        for org in filtered:
            G.add_node(org, publications=org_publication_count[org])

        for o1, o2 in combinations(filtered, 2):
            if G.has_edge(o1, o2):
                G[o1][o2]["weight"] += 1
            else:
                G.add_edge(o1, o2, weight=1)

    print(f"Organizations in graph: {G.number_of_nodes()}")
    print(f"Collaborations (edges): {G.number_of_edges()}")

    if G.number_of_nodes() == 0:
        print("No network to visualize.")
        return

    communities = list(greedy_modularity_communities(G))
    org_cluster = {}

    for i, comm in enumerate(communities):
        for org in comm:
            org_cluster[org] = i

    plt.figure(figsize=(26, 26))
    pos = nx.spring_layout(G, k=0.25, seed=42)

    node_sizes = [G.degree(n) * 20 + 80 for n in G.nodes()]
    node_colors = [org_cluster.get(n, 0) for n in G.nodes()]

    nx.draw_networkx_edges(G, pos, alpha=0.25, width=0.5)
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=plt.cm.tab20,
        alpha=0.9
    )
    nx.draw_networkx_labels(G, pos, font_size=6)

    plt.title(
        f"Organization Network (Min Publications ≥ {min_pubs})",
        fontsize=18
    )
    plt.axis("off")
    plt.show()

    if nx.is_connected(G):
        G_largest = G
    else:
        largest_cc = max(nx.connected_components(G), key=len)
        G_largest = G.subgraph(largest_cc).copy()

    plt.figure(figsize=(26, 26))
    pos_largest = nx.spring_layout(G_largest, k=0.3, seed=42)

    node_sizes_l = [G_largest.degree(n) * 25 + 100 for n in G_largest.nodes()]
    node_colors_l = [org_cluster.get(n, 0) for n in G_largest.nodes()]

    nx.draw_networkx_edges(G_largest, pos_largest, alpha=0.35, width=0.7)
    nx.draw_networkx_nodes(
        G_largest,
        pos_largest,
        node_size=node_sizes_l,
        node_color=node_colors_l,
        cmap=plt.cm.tab20,
        alpha=0.95
    )
    nx.draw_networkx_labels(G_largest, pos_largest, font_size=7)

    plt.title(
        f"Organization Network – Largest Connected Component (Min Publications ≥ {min_pubs})",
        fontsize=18
    )
    plt.axis("off")
    plt.show()

for min_pub in [1, 2, 3]:
    build_and_plot_org_network(min_pub)
