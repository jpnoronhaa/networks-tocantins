import argparse
import os
import csv
import sys
import pandas as pd
import networkx as nx
from src.network_util import evolution_graphs

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
    help='O caminho para o arquivos GEXF de saída com os grafos de coautoria.'
  )

  parser.add_argument(
    '--file-suffix',
    type=str,
    required=True,
    help='Sufixo para os arquivos de saída.'
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
  file_suffix = args.file_suffix
  start_year = args.start_year
  end_year = args.end_year

  new_limit = sys.maxsize
  csv.field_size_limit(new_limit)
  
  try:
    df_works = pd.read_csv(csv_path_works, encoding='utf8', engine='python')
    print(f"DataFrame de trabalhos lido de: {csv_path_works}\n")
    
    df_authors = pd.read_csv(csv_path_authors, encoding='utf8', engine='python')
    print(f"DataFrame de autores lido de: {csv_path_authors}\n")
    
    graphs = evolution_graphs(df_works, df_authors, start_year, end_year)

    try:
      output_gexf_dir = os.path.dirname(output_gexf_path)
      if output_gexf_dir and not os.path.exists(output_gexf_dir):
        os.makedirs(output_gexf_dir)
        print(f"Diretório de saída GEXF '{output_gexf_dir}' criado.")

      print(f"Salvando grafos na pasta: {output_gexf_path}\n")

      for year, graph in graphs.items():
          if graph:
              file_name = f"graph_{file_suffix}_{year}.gexf"
              file_path = os.path.join(output_gexf_path, file_name)
              nx.write_gexf(graph, file_path)
              print(f"Grafo do ano {year} salvo em: {file_path}")
          else:
              print(f"Nenhum grafo gerado para o ano {year}. Arquivo não será salvo.")
      print(f"\nGrafos salvos com sucesso em GEXF: {output_gexf_path}")
    except IOError as e:
      print(f"\nErro ao salvar o arquivo GEXF de saída em '{output_gexf_path}': {e}")
    except Exception as e:
      print(f"\nOcorreu um erro inesperado ao salvar o arquivo GEXF: {e}")
    
  except FileNotFoundError as e:
    print(f"Erro: O arquivo CSV '{e.filename}' não foi encontrado.")
  except pd.errors.EmptyDataError as e:
    print(f"Erro: O arquivo CSV '{e}' está vazio ou contém apenas cabeçalho.")
  except pd.errors.ParserError as e:
    print(f"Erro: Não foi possível analisar o arquivo CSV '{e}'. Verifique o formato. Detalhes: {e}")
  except Exception as e:
    print(f"Erro nao especificado. {e}")


if __name__ == "__main__":
  main()