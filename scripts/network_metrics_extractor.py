import argparse
import os
import networkx as nx
import json
from src.network_util import extract_graph_metrics

def main():
  parser = argparse.ArgumentParser(
    description='Extrai as métricas de um grafo e salva elas como JSON.'
  )

  parser.add_argument(
    '--gexf-path',
    type=str,
    required=True,
    help='O caminho para o arquivo GEXF de entrada do grafo.'
  )

  parser.add_argument(
    '--output-json-path',
    type=str,
    required=True,
    help='O caminho para o arquivo JSON de saída com as métricas do grafo.'
  )
  
  args = parser.parse_args()

  gexf_path = args.gexf_path
  output_json_path = args.output_json_path
  
  try:
    graph = nx.read_gexf(gexf_path)
    print(f"Grafo lido de: {gexf_path}\n")
    
    print(f"Iniciando a coleta das métricas")
    metrics = extract_graph_metrics(graph)

    try:
      output_json_dir = os.path.dirname(output_json_path)
      if output_json_dir and not os.path.exists(output_json_dir):
        os.makedirs(output_json_dir)
        print(f"Diretório de saída JSON '{output_json_dir}' criado.")

      with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=4)
      print(f"\nResultados das métricas salvos com sucesso em JSON: {output_json_path}")
    except IOError as e:
      print(f"\nErro ao salvar o arquivo JSON de saída em '{output_json_path}': {e}")
    except Exception as e:
      print(f"\nOcorreu um erro inesperado ao salvar o arquivo JSON: {e}")
    
  except FileNotFoundError as e:
    print(f"Erro: O arquivo CSV '{e.filename}' não foi encontrado.")
  except Exception as e:
    print(f"Erro nao especificado. {e}")


if __name__ == "__main__":
  main()