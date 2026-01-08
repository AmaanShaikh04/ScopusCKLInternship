# File name: test.py
import pandas as pd
import re

file_path = "285scopus_wearables_ai_education_corpus.csv"

for enc in ["utf-8", "latin1"]:
    try:
        df = pd.read_csv(file_path, encoding=enc)
        print(f"Loaded with {enc}")
        break
    except:
        continue

AUTHOR_COL = "Author full names"
AFFIL_COL = "Authors with affiliations"

if AUTHOR_COL not in df.columns or AFFIL_COL not in df.columns:
    raise ValueError("The file does not contain expected columns.")

def split_authors(text):
    if not isinstance(text, str):
        return []
    return [a.strip() for a in re.split(r'[;,]', text) if len(a.strip()) > 2]

df["Author_List"] = df[AUTHOR_COL].apply(split_authors)

author_counts = {}

for authors in df["Author_List"]:
    for a in authors:
        author_counts[a] = author_counts.get(a, 0) + 1

author_counts_df = (
    pd.DataFrame.from_dict(author_counts, orient="index", columns=["Publications"])
    .sort_values("Publications", ascending=False)
)

top_authors = author_counts_df.head(20).copy()

def extract_affiliation(author, affil_text):
    """Return affiliation that contains the author's name."""
    if not isinstance(affil_text, str):
        return ""
    lines = affil_text.split(";")
    for line in lines:
        if author.lower() in line.lower():
            cleaned = re.sub(r"\([^)]*\)", "", line)
            return cleaned.strip()
    return ""


affiliation_map = {}

for _, row in df.iterrows():
    affil_text = row[AFFIL_COL]
    authors = row["Author_List"]
    for a in authors:
        if a not in affiliation_map:
            affil = extract_affiliation(a, affil_text)
            if affil:
                affiliation_map[a] = affil

top_authors["Affiliation"] = top_authors.index.map(lambda x: affiliation_map.get(x, ""))

output_file = "key_authors_preliminary.csv"
top_authors.to_csv(output_file)

print(f"\nSaved {output_file}")
print(top_authors)
