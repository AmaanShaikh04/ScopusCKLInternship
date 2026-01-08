# File name: interactiveanalysis.py
import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = "285scopus_wearables_ai_education_corpus.csv"
outdir = "analysis_results"
os.makedirs(outdir, exist_ok=True)

try:
    df = pd.read_csv(file_path, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding="latin1")

print(f"Loaded {file_path} with columns:\n{list(df.columns)}")

if "Year" in df.columns:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    year_counts = df["Year"].value_counts().sort_index()
    if not year_counts.empty:
        print("\nPapers by Year:\n", year_counts)
        year_counts.to_csv(os.path.join(outdir, "papers_by_year.csv"))
        year_counts.plot(kind="bar", figsize=(8, 5), color="skyblue", title="Papers by Year")
        plt.tight_layout()
        plt.show()
    else:
        print("No valid year data found.")
else:
    print("'Year' column not found in CSV.")

journal_col = None
for c in df.columns:
    if "source" in c.lower() or "journal" in c.lower():
        journal_col = c
        break

if journal_col:
    top_journals = df[journal_col].dropna().value_counts().head(15)
    print("\nTop Journals:\n", top_journals)
    top_journals.to_csv(os.path.join(outdir, "top_journals.csv"), header=["Count"])
    top_journals.sort_values().plot(kind="barh", figsize=(8, 5), color="coral", title="Top Journals")
    plt.tight_layout()
    plt.show()
else:
    print("No journal/source column found.")

if "Authors" in df.columns:
    author_list = (
        df["Authors"]
        .dropna()
        .astype(str)
        .str.split(";")
        .explode()
        .str.strip()
    )

    author_list = author_list[author_list.str.len() > 2]

    top_authors = author_list.value_counts().head(20)
    print("\nTop Authors (Full Names):\n", top_authors)

    try:
        top_authors.to_csv(os.path.join(outdir, "top_authors.csv"), header=["Count"])
    except PermissionError:
        backup_path = os.path.join(outdir, "top_authors_backup.csv")
        top_authors.to_csv(backup_path, header=["Count"])
        print(f"Saved backup as {backup_path}")

    top_authors.sort_values().plot(kind="barh", figsize=(8, 6), color="lightgreen", title="Top Authors")
    plt.tight_layout()
    plt.show()
else:
    print("No 'Authors' column found in CSV.")

inst_col = None
for c in df.columns:
    if "affiliation" in c.lower() or "institution" in c.lower():
        inst_col = c
        break

if inst_col:
    inst_list = (
        df[inst_col]
        .dropna()
        .astype(str)
        .str.split(";")
        .explode()
        .str.strip()
    )
    inst_list = inst_list[inst_list.str.len() > 2]
    top_institutions = inst_list.value_counts().head(15)
    print("\nTop Institutions:\n", top_institutions)

    top_institutions.to_csv(os.path.join(outdir, "top_institutions.csv"), header=["Count"])
    top_institutions.sort_values().plot(kind="barh", figsize=(8, 5), color="orange", title="Top Institutions")
    plt.tight_layout()
    plt.show()
else:
    print("No institution/affiliation column found.")

country_col = None
for c in df.columns:
    if "country" in c.lower():
        country_col = c
        break

if country_col:
    top_countries = df[country_col].dropna().value_counts().head(15)
    print("\nTop Countries:\n", top_countries)
    top_countries.to_csv(os.path.join(outdir, "top_countries.csv"), header=["Count"])
    top_countries.sort_values().plot(kind="barh", figsize=(8, 5), color="violet", title="Top Countries")
    plt.tight_layout()
    plt.show()
else:
    print("No country column found in the data.")

print("\nInteractive analysis complete! All summaries saved to 'analysis_results' folder.\n")
