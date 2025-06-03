import networkx as nx
import pandas as pd
from src.works_util import count_papers_by_year


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
  # TODO: implementar código para gerar um grafo de coautoria
  graph = nx.Graph()
  
  return graph


def evelution_graphs(df_works, df_authors, start_year, end_year):
  
  graphs = {}
  year_counts = count_papers_by_year(df_works, start_year, end_year)
  
  for year, year_works in year_counts.items():
    
    if year_works == 0:
      continue
    
    df_works_filtered = df_works[df_works['publication_year'] <= year]
    graph = generate_coauthorship_graph(df_works_filtered, df_authors)
    graphs[year] = graph
    
  
  return graphs