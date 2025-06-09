import pandas as pd
import argparse
import os
import csv
import sys
import json
from src.institutions_util import count_institutions, analyze_institution_papers

def main():
  parser = argparse.ArgumentParser(
    description='Extrai e analisa dados de trabalhos científicos e exporta os resultados como JSON.'
  )

  parser.add_argument(
    '--csv-path',
    type=str,
    required=True,
    help='O caminho para o arquivo CSV de entrada.'
  )

  parser.add_argument(
    '--output-json-path',
    type=str,
    required=True,
    help='O caminho para o arquivo JSON de saída com os resultados das análises.'
  )

  parser.add_argument(
    '--target-institutions',
    type=str,
    nargs='+',
    help='Uma lista de nomes de instituições para análise específica (separadas por espaço). Ex: "Instituto Federal do Tocantins" "Universidade Federal do Tocantins"'
  )

  args = parser.parse_args()

  csv_path = args.csv_path
  output_json_path = args.output_json_path
  target_institutions = args.target_institutions if args.target_institutions else []

  new_limit = sys.maxsize
  try:
    csv.field_size_limit(new_limit)
    df_works = pd.read_csv(csv_path, encoding='utf8', engine='python')
    print(f"DataFrame lido de: {csv_path}\n")
    
    analysis_results = {}

    if 'authorships.institutions' in df_works.columns:
      print("Realizando a contagem de trabalhos por instituição...")
      institution_counts = count_institutions(df_works)
      analysis_results['institution_counts'] = institution_counts
      print("Contagem de instituições concluída.")
    else:
      print("Coluna 'authorships.institutions' não encontrada. Pulando a contagem de instituições.")

    if 'authorships.institutions' in df_works.columns and target_institutions:
      print(f"Realizando a análise para as instituições alvo: {target_institutions}...")
      target_analysis = analyze_institution_papers(df_works, target_institutions)
      analysis_results['target_institution_analysis'] = target_analysis
      print("Análise de instituições alvo concluída.")
    elif not target_institutions:
      print("Nenhuma instituição alvo fornecida. Pulando a análise de instituições alvo.")
    else:
      print("Coluna 'authorships.institutions' não encontrada. Pulando a análise de instituições alvo.")

    try:
      output_json_dir = os.path.dirname(output_json_path)
      if output_json_dir and not os.path.exists(output_json_dir):
        os.makedirs(output_json_dir)
        print(f"Diretório de saída JSON '{output_json_dir}' criado.")

      with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=4)
      print(f"\nResultados das análises salvos com sucesso em JSON: {output_json_path}")
    except IOError as e:
      print(f"\nErro ao salvar o arquivo JSON de saída em '{output_json_path}': {e}")
    except Exception as e:
      print(f"\nOcorreu um erro inesperado ao salvar o arquivo JSON: {e}")
    
  except FileNotFoundError:
    print(f"Erro: O arquivo CSV '{csv_path}' não foi encontrado.")
  except pd.errors.EmptyDataError:
    print(f"Erro: O arquivo CSV '{csv_path}' está vazio ou contém apenas cabeçalho.")
  except pd.errors.ParserError as e:
    print(f"Erro: Não foi possível analisar o arquivo CSV '{csv_path}'. Verifique o formato. Detalhes: {e}")
  except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
  main()