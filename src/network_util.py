import networkx as nx
import pandas as pd
from src.works_util import count_papers_by_year
from src.authorship_util import extract_authors_ids
from itertools import combinations


def generate_coauthorship_graph(df_works, df_authors):
  """Gera um grafo de coautoria a partir de DataFrames de trabalhos e autores.

  Args:
    df_works (pd.DataFrame): DataFrame contendo informações sobre os trabalhos.
    df_authors (pd.DataFrame): DataFrame contendo informações sobre os autores.

  Returns:
    nx.Graph: Um grafo NetworkX representando a rede de coautoria,
            onde os nós são autores e as arestas são ponderadas
            pela quantidade de coautorias. Os nós possuem atributos
            com as informações dos autores.
  """
  graph = nx.Graph()
  authors_ids_set = extract_authors_ids(df_works)

  for _, row in df_authors.iterrows():
    author_id = row.get('id', '') if pd.notna(row.get('id')) else ''
    
    if author_id not in authors_ids_set:
      continue
    
    author_attributes = {
      'author_display_name' : row.get('display_name', '') if pd.notna(row.get('display_name')) else '',
      'author_institution_display_name' : row.get('institution_display_name', '') if pd.notna(row.get('institution_display_name')) else '',
      'author_institution_country_code' : row.get('institution_country_code', '') if pd.notna(row.get('institution_country_code')) else '',
      'author_raw_author_name' : row.get('raw_author_name', '') if pd.notna(row.get('raw_author_name')) else '',
      'author_institution_id' : row.get('institution_id', '') if pd.notna(row.get('institution_id')) else '',
      'author_country' : row.get('country', '') if pd.notna(row.get('country')) else '',
      'author_orcid' : row.get('orcid', '') if pd.notna(row.get('orcid')) else ''
    }

    graph.add_node(author_id, **author_attributes)

  for _, row in df_works.iterrows():
    authors_ids = row.get('authorships.author.id', '').split('|') if pd.notna(row.get('authorships.author.id')) else []

    for author1_id, author2_id in combinations(authors_ids, 2):
      if graph.has_node(author1_id) and graph.has_node(author2_id):
        if graph.has_edge(author1_id, author2_id):
          graph[author1_id][author2_id]['weight'] += 1
        else:
          graph.add_edge(author1_id, author2_id, weight=1)

  return graph


def evolution_graphs(df_works, df_authors, start_year, end_year):
  graphs = {}
  df_works['publication_year'] = pd.to_numeric(df_works['publication_year'], errors='coerce')
  df_works.dropna(subset=['publication_year'], inplace=True)
  df_works['publication_year'] = df_works['publication_year'].astype(int)
  year_counts = count_papers_by_year(df_works, start_year, end_year)
  
  for year, year_works in year_counts.items():
    
    if year_works == 0:
      continue

    df_works_filtered = df_works[df_works['publication_year'] <= year]
    graph = generate_coauthorship_graph(df_works_filtered, df_authors)
    graphs[year] = graph
    
  
  return graphs