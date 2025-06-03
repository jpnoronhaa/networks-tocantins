import argparse
import os
import csv
import sys
import pandas as pd
from src.network_util import evelution_graphs

def main():
  parser = argparse.ArgumentParser(
    description='Monta um grafo de coautoria em um determinado período de tempo e exporta os dados em formato GEXF.'
  )

  parser.add_argument(
    '--csv-path-works',
    type=str,
    required=True,
    help='O caminho para o arquivo CSV de entrada dos trabalhos.'
  )
  
  parser.add_argument(
    '--csv-path-authors',
    type=str,
    required=True,
    help='O caminho para o arquivo CSV de entrada dos autores.'
  )

  parser.add_argument(
    '--output-gexf-path',
    type=str,
    required=True,
    help='O caminho para o arquivo GEXF de saída com o grafo de coautoria.'
  )

  parser.add_argument(
    '--start-year',
    type=int,
    default=1998,
    help='O ano de início para a modelagem do grafo por ano (inclusive).'
  )

  parser.add_argument(
    '--end-year',
    type=int,
    default=2024,
    help='O ano de término para a modelagem do grafo por ano (inclusive).'
  )
  
  args = parser.parse_args()

  csv_path_works = args.csv_path_works
  csv_path_authors = args.csv_path_authors
  output_gexf_path = args.output_gexf_path
  start_year = args.start_year
  end_year = args.end_year

  new_limit = sys.maxsize
  csv.field_size_limit(new_limit)
  
  try:
    df_works = pd.read_csv(csv_path_works, encoding='utf8', engine='python')
    print(f"DataFrame de trabalhos lido de: {csv_path_works}\n")
    
    df_authors = pd.read_csv(csv_path_authors, encoding='utf8', engine='python')
    print(f"DataFrame de autores lido de: {csv_path_authors}\n")
    
    graphs = evelution_graphs(df_works, df_authors, start_year, end_year)
    
  except FileNotFoundError as e:
    print(f"Erro: O arquivo CSV '{e.filename}' não foi encontrado.")
  except pd.errors.EmptyDataError as e:
    print(f"Erro: O arquivo CSV '{e}' está vazio ou contém apenas cabeçalho.")
  except pd.errors.ParserError as e:
    print(f"Erro: Não foi possível analisar o arquivo CSV '{e}'. Verifique o formato. Detalhes: {e}")
  except Exception as e:a um grafo de coautoria 