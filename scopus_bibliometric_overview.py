# File name: analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import itertools
import networkx as nx

def load_file(filepath):
    for enc in ["utf-8", "latin1"]:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            print(f"Loaded {filepath} with encoding {enc}")
            return df
        except Exception as e:
            print(f"Failed to load with {enc}: {e}")
    raise ValueError("Could not read the CSV file.")


def papers_by_year(df, outdir):
    year_cols = [c for c in df.columns if "year" in c.lower()]
    if not year_cols:
        return

    col = year_cols[0]
    df[col] = pd.to_numeric(df[col], errors="coerce")
    counts = df[col].value_counts().sort_index()

    if counts.empty:
        return

    counts.plot(kind="bar", figsize=(8, 5))
    plt.xlabel("Publication Year")
    plt.ylabel("Number of Papers")
    plt.title("Publications by Year")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "papers_by_year.png"), dpi=200)
    plt.close()

def top_journals(df, outdir, topn=15):
    journal_cols = [c for c in df.columns if "journal" in c.lower() or "source title" in c.lower()]
    if not journal_cols:
        return

    col = journal_cols[0]
    counts = df[col].dropna().astype(str).value_counts().head(topn)

    if counts.empty:
        return

    counts.sort_values().plot(kind="barh", figsize=(8, 5))
    plt.xlabel("Number of Papers")
    plt.title("Top Journals")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "top_journals.png"), dpi=200)
    plt.close()

def top_authors_with_latest_papers(df, outdir, topn=20):
    author_cols = [c for c in df.columns if "author" in c.lower()]
    year_cols = [c for c in df.columns if "year" in c.lower()]
    title_cols = [c for c in df.columns if "title" in c.lower()]

    if not author_cols or not year_cols or not title_cols:
        print("Missing required columns for author analysis.")
        return

    author_col = author_cols[0]
    year_col = year_cols[0]
    title_col = title_cols[0]

    rows = []

    for _, row in df.iterrows():
        if pd.isna(row[author_col]):
            continue

        authors = [a.strip() for a in re.split(r"[;,]", str(row[author_col])) if len(a.strip()) > 2]
        for a in authors:
            rows.append({
                "author": a,
                "year": row[year_col],
                "title": row[title_col]
            })

    author_df = pd.DataFrame(rows)
    author_df["year"] = pd.to_numeric(author_df["year"], errors="coerce")

    top_authors = author_df["author"].value_counts().head(topn).index.tolist()

    output_rows = []
    for author in top_authors:
        sub = author_df[author_df["author"] == author].sort_values("year", ascending=False)
        latest_titles = sub["title"].dropna().head(3).tolist()

        output_rows.append({
            "Author": author,
            "Publications": len(sub),
            "Latest Paper 1": latest_titles[0] if len(latest_titles) > 0 else "",
            "Latest Paper 2": latest_titles[1] if len(latest_titles) > 1 else "",
            "Latest Paper 3": latest_titles[2] if len(latest_titles) > 2 else "",
        })

    out_df = pd.DataFrame(output_rows)
    out_df.to_csv(os.path.join(outdir, "top_authors_with_latest_papers.csv"), index=False)
    print("Saved top_authors_with_latest_papers.csv")

def author_coauthorship_network(df, outdir, min_edges=2):
    author_cols = [c for c in df.columns if "author" in c.lower()]
    if not author_cols:
        print("No author column found.")
        return

    author_col = author_cols[0]
    edge_counter = {}

    for authors_str in df[author_col].dropna():
        authors = [a.strip() for a in re.split(r"[;,]", str(authors_str)) if len(a.strip()) > 2]
        for a, b in itertools.combinations(sorted(authors), 2):
            edge_counter[(a, b)] = edge_counter.get((a, b), 0) + 1

    edges = [
        {"Author_1": a, "Author_2": b, "Weight": w}
        for (a, b), w in edge_counter.items()
        if w >= min_edges
    ]

    if not edges:
        print("No co-author edges found.")
        return

    edge_df = pd.DataFrame(edges)
    edge_df.to_csv(os.path.join(outdir, "author_coauthorship_edges.csv"), index=False)

    G = nx.Graph()
    for _, row in edge_df.iterrows():
        G.add_edge(row["Author_1"], row["Author_2"], weight=row["Weight"])

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.4, seed=42)

    weights = [d["weight"] for _, _, d in G.edges(data=True)]
    nx.draw_networkx_nodes(G, pos, node_size=200)
    nx.draw_networkx_edges(G, pos, width=[w * 0.5 for w in weights], alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=7)

    plt.title("Co-authorship Network")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "author_coauthorship_network.png"), dpi=200)
    plt.close()

    print("Saved author co-authorship network (CSV + PNG)")

def main():
    file_path = "285scopus_wearables_ai_education_corpus.csv"
    outdir = "analysis_results"
    os.makedirs(outdir, exist_ok=True)

    df = load_file(file_path)
    print(f"Columns detected: {list(df.columns)}")

    papers_by_year(df, outdir)
    top_journals(df, outdir)
    top_authors_with_latest_papers(df, outdir)
    author_coauthorship_network(df, outdir)

    print("\nAnalysis complete. Check 'analysis_results' folder.")


if __name__ == "__main__":
    main()
