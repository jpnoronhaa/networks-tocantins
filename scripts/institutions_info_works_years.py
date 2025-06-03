import pandas as pd
import argparse
import os
import csv
import sys
import json
from src.works_util import count_papers_by_year

def main():
  parser = argparse.ArgumentParser(
    description='Extrai a quantidade de trabalhos publicados ao longo dos anos e exporta os resultados como JSON.'
  )

  parser.add_argument(
    '--csv-paths',
    type=str,
    nargs='+',
    required=True,
    help='Uma lista de caminhos para os arquivos CSV de entrada (separados por espaço).'
  )

  parser.add_argument(
    '--output-json-path',
    type=str,
    required=True,
    help='O caminho para o arquivo JSON de saída com os resultados das análises.'
  )

  parser.add_argument(
    '--start-year',
    type=int,
    default=1998,
    help='O ano de início para a análise de trabalhos por ano (inclusive).'
  )

  parser.add_argument(
    '--end-year',
    type=int,
    default=2024,
    help='O ano de término para a análise de trabalhos por ano (inclusive).'
  )

  args = parser.parse_args()

  csv_paths = args.csv_paths
  output_json_path = args.output_json_path
  start_year = args.start_year
  end_year = args.end_year

  new_limit = sys.maxsize
  all_analysis_results = {}
  csv.field_size_limit(new_limit)


  for i, csv_path in enumerate(csv_paths):
    try:
      df_works = pd.read_csv(csv_path, encoding='utf8', engine='python')
      print(f"DataFrame lido de: {csv_path}\n")
      
      file_name = os.path.basename(csv_path).replace('.csv', '')

      print(f"Realizando a contagem de trabalhos por ano para {file_name} entre {start_year} e {end_year}...")
      year_counts = count_papers_by_year(df_works, start_year, end_year)
      print("Contagem de trabalhos por ano concluída.")
        
      all_analysis_results[file_name] = year_counts

    except FileNotFoundError:
      print(f"Erro: O arquivo CSV '{csv_path}' não foi encontrado.")
    except pd.errors.EmptyDataError:
      print(f"Erro: O arquivo CSV '{csv_path}' está vazio ou contém apenas cabeçalho.")
    except pd.errors.ParserError as e:
      print(f"Erro: Não foi possível analisar o arquivo CSV '{csv_path}'. Verifique o formato. Detalhes: {e}")
    except Exception as e:
      print(f"Ocorreu um erro inesperado ao processar '{csv_path}': {e}")
            
    try:
      output_json_dir = os.path.dirname(output_json_path)
      if output_json_dir and not os.path.exists(output_json_dir):
        os.makedirs(output_json_dir)
        print(f"Diretório de saída JSON '{output_json_dir}' criado.")

      with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_analysis_results, f, ensure_ascii=False, indent=4)
      print(f"\nTodos os resultados das análises salvos com sucesso em JSON: {output_json_path}")
    except IOError as e:
      print(f"\nErro ao salvar o arquivo JSON de saída em '{output_json_path}': {e}")
    except Exception as e:
      print(f"\nOcorreu um erro inesperado ao salvar o arquivo JSON: {e}")

if __name__ == "__main__":
  main()