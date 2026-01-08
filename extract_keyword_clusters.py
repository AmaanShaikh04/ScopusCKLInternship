# File name: keywordFetch.py
import pandas as pd
import networkx as nx
from itertools import combinations

file_path = "keyword_network_edges.csv"
df = pd.read_csv(file_path)

df.columns = [c.strip() for c in df.columns]

G = nx.Graph()

for _, row in df.iterrows():
    G.add_edge(row["source"] if "source" in df.columns else row["kw1"],
               row["target"] if "target" in df.columns else row["kw2"],
               weight=row["weight"] if "weight" in df.columns else 1)

top_pairs = sorted(G.edges(data=True), key=lambda x: x[2].get("weight", 0), reverse=True)[:10]

print("\nTop Keyword Pairs (by co-occurrence weight):")
for i, (a, b, d) in enumerate(top_pairs, 1):
    print(f"{i}. ({a}, {b}) - {d['weight']}")

components = list(nx.connected_components(G))
components = sorted(components, key=len, reverse=True)

print("\nTop Keyword Clusters (Groups of related terms):")
for i, comp in enumerate(components[:5], 1):
    print(f"Cluster {i}: {', '.join(comp)}")

print("\nSuggested Keyword Combinations for Search Queries:")
for i, comp in enumerate(components[:3], 1):
    combo = " OR ".join([f'\"{kw}\"' for kw in list(comp)[:5]])
    print(f"({combo})")
