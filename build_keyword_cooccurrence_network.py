# File name: graph.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import community


file_path = "manual_seed_papers_keywords.csv"
try:
    df = pd.read_csv(file_path, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding="latin1")

df.columns = [c.strip() for c in df.columns]

df["All_Keywords"] = (
    df["Author Keywords"].fillna('') + ',' + df["Indexed Keywords"].fillna('')
)

def clean_keywords(keyword_string):
    if not isinstance(keyword_string, str):
        return []
    words = keyword_string.lower().replace(";", ",").split(",")
    stopwords = {
        "", "study", "article", "education", "learning", "students",
        "teacher", "teaching", "human", "humans", "system", "data",
        "analysis", "approach", "research", "technology"
    }
    cleaned = [w.strip() for w in words if w.strip() not in stopwords]
    return list(set(cleaned))

df["Keyword_List"] = df["All_Keywords"].apply(clean_keywords)

pairs = []
for kws in df["Keyword_List"]:
    for combo in combinations(sorted(set(kws)), 2):
        pairs.append(combo)

pairs_df = pd.DataFrame(pairs, columns=["kw1", "kw2"])

pair_counts = pairs_df.value_counts().reset_index(name="weight")

G = nx.Graph()

for _, row in pair_counts.iterrows():
    G.add_edge(row["kw1"], row["kw2"], weight=row["weight"])

G.remove_edges_from([(u, v) for u, v, w in G.edges(data="weight") if w < 2])

isolated = list(nx.isolates(G))
G.remove_nodes_from(isolated)

print(f"Network built with {len(G.nodes())} keywords and {len(G.edges())} connections.")

partition = community.best_partition(G)
colors = [partition[n] for n in G.nodes()]

plt.figure(figsize=(13, 10))
pos = nx.spring_layout(G, k=0.4, seed=42)

sizes = [G.degree(n) * 120 for n in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color=colors, cmap=plt.cm.tab10, alpha=0.85)
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.3)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

plt.title("Keyword Co-Occurrence Network (Author + Indexed Keywords)", fontsize=14, pad=20)
plt.axis("off")
plt.tight_layout()
plt.show()

edges_out = nx.to_pandas_edgelist(G)
edges_out.to_csv("keyword_network_edges.csv", index=False)
print("Exported keyword_network_edges.csv with all keyword links.")
