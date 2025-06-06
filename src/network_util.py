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

def extract_graph_metrics(graph):
  """
  Calcula e retorna diversas métricas de um grafo.

  Args:
  graph (nx.Graph): O grafo NetworkX do qual as métricas serão extraídas.

  Returns:
    dict: Um dicionário contendo as seguintes métricas do grafo:
    - 'num_nodes': Número de vértices no grafo.
    - 'num_edges': Número de arestas no grafo.
    - 'largest_connected_component_size': Tamanho da maior componente conexa.
    - 'degrees': Dicionário com o grau de cada vértice.
    - 'average_degree': Grau médio do grafo.
    - 'degree_distribution': Dicionário com a distribuição de graus.
    - 'local_clustering_coefficient': Dicionário com o coeficiente de agrupamento local de cada vértice.
    - 'average_clustering_coefficient': Coeficiente de agrupamento médio da rede.
    - 'average_shortest_path_length': Menor caminho médio (apenas para componentes conectados).
    - 'betweenness_centrality': Dicionário com a centralidade de intermediação de cada vértice.
    - 'closeness_centrality': Dicionário com a centralidade de proximidade de cada vértice.
    - 'eigenvector_centrality': Dicionário com a centralidade de autovetor de cada vértice.
    - 'degree_assortativity_coefficient': Coeficiente de assortatividade por grau.
  """
  metrics = {}

  print('Coleta de dados: números de vértices e arestas')
  metrics['num_nodes'] = graph.number_of_nodes()
  metrics['num_edges'] = graph.number_of_edges()

  print('Coleta de dados: maior componente conexa')

  if graph.number_of_nodes() > 0:
    connected_components = list(nx.connected_components(graph))
    if connected_components:
      metrics['largest_connected_component_size'] = len(max(connected_components, key=len))
    else:
      metrics['largest_connected_component_size'] = 0
  else:
    metrics['largest_connected_component_size'] = 0

  print('Coleta de dados: grau, grau médio e distribuição de graus')
  degrees = dict(graph.degree())
  metrics['degrees'] = degrees
  metrics['average_degree'] = sum(d for n, d in graph.degree()) / len(graph) if len(graph) > 0 else 0

  degree_counts = nx.degree_histogram(graph)
  degree_distribution = {i: count for i, count in enumerate(degree_counts) if count > 0}
  metrics['degree_distribution'] = degree_distribution

  metrics['local_clustering_coefficient'] = nx.clustering(graph)

  metrics['average_clustering_coefficient'] = nx.average_clustering(graph)

  print('Coleta de dados: média da distância geodésica')
  if nx.is_connected(graph):
    metrics['average_shortest_path_length'] = nx.average_shortest_path_length(graph)
  else:
    components = [graph.subgraph(c).copy() for c in nx.connected_components(graph)]
    if components:
      largest_component = max(components, key=len)
      if len(largest_component) > 1:
        metrics['average_shortest_path_length'] = nx.average_shortest_path_length(largest_component)
      else:
        metrics['average_shortest_path_length'] = None
    else:
      metrics['average_shortest_path_length'] = None

  print('Coleta de dados: centralidades')
  metrics['betweenness_centrality'] = nx.betweenness_centrality(graph)
  metrics['closeness_centrality'] = nx.closeness_centrality(graph)
  
  try:
    metrics['eigenvector_centrality'] = nx.eigenvector_centrality(graph)
  except nx.PowerIterationFailedConvergence:
    metrics['eigenvector_centrality'] = "Could not converge"
  except ValueError:
    metrics['eigenvector_centrality'] = {}

  print('Coleta de dados: assortatividade')
  metrics['degree_assortativity_coefficient'] = nx.degree_assortativity_coefficient(graph)

  return metrics