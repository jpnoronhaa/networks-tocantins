import pandas as pd
from src.authorship import extract_authors
import argparse
import os

def main():
  parser = argparse.ArgumentParser(
    description='Extrai a lista de autores de uma lista de trabalhos e exporta os dados como CSV.'
  )

  parser.add_argument(
    '--csv-path',
    type=str,
    required=True,
    help='O caminho para o arquivo CSV de entrada.'
  )

  parser.add_argument(
    '--output-csv-path',
    type=str,
    required=True,
    help='O caminho para o arquivo CSV de saída com os autores.'
  )

  args = parser.parse_args()

  csv_path = args.csv_path
  output_csv_path = args.output_csv_path

  try:
    df_works = pd.read_csv(csv_path)
    print(f"DataFrame lido de: {csv_path}\n")
    print("Extraindo os autores do arquivo de entrada...")
    authors_frozenset = extract_authors(df_works)
    
    authors_list_of_dicts = [dict(item) for item in authors_frozenset]
    authors_df = pd.DataFrame(authors_list_of_dicts)
    
    print("\nLista de Autores Gerada (Exemplo de Saída no Terminal):")
    print(authors_df.head())

    try:
      output_csv_dir = os.path.dirname(output_csv_path)
      if output_csv_dir and not os.path.exists(output_csv_dir):
        os.makedirs(output_csv_dir)
        print(f"Diretório de saída CSV '{output_csv_dir}' criado.")

      authors_df.to_csv(output_csv_path, index=False, encoding='utf-8')
      print(f"Lista de autores salva com sucesso em CSV: {output_csv_path}")
    except IOError as e:
      print(f"\nErro ao salvar o arquivo CSV de saída em '{output_csv_path}': {e}")
    except Exception as e:
      print(f"\nOcorreu um erro inesperado ao salvar o arquivo CSV: {e}")
    
  except FileNotFoundError:
    print(f"Erro: O arquivo CSV '{csv_path}' não foi encontrado.")
  except pd.errors.EmptyDataError:
    print(f"Erro: O arquivo CSV '{csv_path}' está vazio ou contém apenas cabeçalho.")
  except pd.errors.ParserError:
    print(f"Erro: Não foi possível analisar o arquivo CSV '{csv_path}'. Verifique o formato.")
  except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
  main()