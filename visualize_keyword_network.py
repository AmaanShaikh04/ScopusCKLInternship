# File name: keyword_network_graph.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community

file_path = "keyword_network_edges.csv"
df = pd.read_csv(file_path, encoding="latin1")

src_col = "source" if "source" in df.columns else "kw1"
tgt_col = "target" if "target" in df.columns else "kw2"
wgt_col = "weight" if "weight" in df.columns else df.columns[-1]

G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row[src_col], row[tgt_col], weight=row[wgt_col])

communities = community.greedy_modularity_communities(G)

node_colors = []
color_map = {}
for i, c in enumerate(communities):
    for node in c:
        color_map[node] = i
for node in G.nodes():
    node_colors.append(color_map.get(node, 0))

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=0.3, seed=42)

nx.draw_networkx_nodes(G, pos,
                       node_color=node_colors,
                       cmap=plt.cm.Set3,
                       node_size=600,
                       alpha=0.9)
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_labels(G, pos, font_size=9)

plt.title("Keyword Co-occurrence Network", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.savefig("keyword_network_graph.png", dpi=300)
plt.show()
