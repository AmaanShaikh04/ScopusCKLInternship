# Bibliometric Analysis: Wearables, AI, and Education

A comprehensive bibliometric analysis workflow for research at the intersection of **wearables, artificial intelligence (AI), and education**. This repository provides statistical overviews, keyword networks, and author/affiliation collaboration analyses.

---

## Project Overview

This project performs a bibliometric analysis on publications related to **wearables, AI, and education**. It provides:

- Statistical summaries of research output  
- Quality and exploratory data checks  
- Keyword co-occurrence networks and thematic clusters  
- Interactive author and institutional collaboration networks  

The analysis is organized into three phases for clarity and reproducibility.

---

## Installation

Before running any scripts, install the required dependencies. Using a virtual environment is recommended:


## Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install required packages
pip install -r requirements.txt


## Project Workflow
### Phase 1: Initial Analysis
Input: /285scopus_wearables_ai_education_corpus.csv
1. scopus_bibliometric_overview.py - Generates comprehensive bibliometric statistics
2. exploratory_bibliometric_checks.py - Performs data quality checks and validation

### Phase 2: Keyword Network Analysis
Input: /manual_seed_papers_keywords.csv
1. build_keyword_cooccurrence_network.py - Constructs keyword co-occurrence network
2. visualize_keyword_network.py - Creates visualizations of keyword relationships
3. extract_keyword_clusters.py - Identifies and extracts thematic keyword clusters

### Phase 3: Author & Affiliation Analysis
Input: /285scopus_wearables_ai_education_corpus.csv
1. author_affiliation_extraction_test.py - Tests author and affiliation parsing
2. author_network_interactive.py - Builds interactive author collaboration network
3. organization_network_interactive.py - Builds interactive institutional collaboration network

## Execution Order
First, install dependencies:
pip install -r requirements.txt

### Run Phase 1 scripts:
python scopus_bibliometric_overview.py
python exploratory_bibliometric_checks.py

### Run Phase 2 scripts:
python build_keyword_cooccurrence_network.py
python visualize_keyword_network.py
python extract_keyword_clusters.py

### Run Phase 3 scripts:
python author_affiliation_extraction_test.py
python author_network_interactive.py
python organization_network_interactive.py


## Data Files Required
Place these files in the / directory:
285scopus_wearables_ai_education_corpus.csv (Scopus extracted papers)
manual_seed_papers_keywords.csv (Manually scraped papers with keywords)

## Output
Results will be generated in:

1. Console outputs for statistical summaries
2. analysis_results/ folder for visualizations
3. Interactive windows for network visualizations

Note: Some scripts open interactive matplotlib windows. Allow pop-ups if running in certain IDEs or environments.

### For questions or continuation of this work, please refer to the repository structure and scripts above. This project is designed to be extensible for future research in bibliometric analysis.
