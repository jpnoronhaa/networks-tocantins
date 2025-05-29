import pandas as pd
from src.generate_dict import generate_variable_dictionary
import argparse
import os

def main():
  parser = argparse.ArgumentParser(
      description='Gera metadados de variáveis a partir de um arquivo CSV e exporta para CSV e Markdown.'
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
    help='O caminho para o arquivo CSV de saída dos metadados.'
  )

  parser.add_argument(
    '--output-md-path',
    type=str,
    required=True,
    help='O caminho para o arquivo Markdown de saída da tabela de metadados.'
  )

  args = parser.parse_args()

  csv_path = args.csv_path
  output_csv_path = args.output_csv_path
  output_md_path = args.output_md_path

  try:
    df = pd.read_csv(csv_path)
    print(f"DataFrame lido de: {csv_path}\n")
    print("Gerando dicionário de variáveis...")
    variable_dict = generate_variable_dictionary(df)

    metadata_list = [v for k, v in variable_dict.items()]
    metadata_df = pd.DataFrame(metadata_list)

    print("\nMetadados de Variáveis Gerados (Exemplo de Saída no Terminal):")
    print(metadata_df.head())

    try:
      output_csv_dir = os.path.dirname(output_csv_path)
      if output_csv_dir and not os.path.exists(output_csv_dir):
        os.makedirs(output_csv_dir)
        print(f"Diretório de saída CSV '{output_csv_dir}' criado.")

      metadata_df.to_csv(output_csv_path, index=False, encoding='utf-8')
      print(f"Metadados de variáveis salvos com sucesso em CSV: {output_csv_path}")
    except IOError as e:
      print(f"\nErro ao salvar o arquivo CSV de saída em '{output_csv_path}': {e}")
    except Exception as e:
      print(f"\nOcorreu um erro inesperado ao salvar o arquivo CSV: {e}")

    try:
      output_md_dir = os.path.dirname(output_md_path)
      if output_md_dir and not os.path.exists(output_md_dir):
        os.makedirs(output_md_dir)
        print(f"Diretório de saída Markdown '{output_md_dir}' criado.")

      markdown_table = metadata_df.to_markdown(index=False)
      with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write("# Dicionário de Variáveis\n\n")
        f.write(markdown_table)
      print(f"Tabela de metadados salva com sucesso em Markdown: {output_md_path}")
    except IOError as e:
      print(f"\nErro ao salvar o arquivo Markdown de saída em '{output_md_path}': {e}")
    except Exception as e:
      print(f"\nOcorreu um erro inesperado ao salvar o arquivo Markdown: {e}")

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