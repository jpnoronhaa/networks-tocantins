import argparse
import os
import json
import networkx as nx
from src.network_util import identify_hubs, analyze_network_attack

def main():
  parser = argparse.ArgumentParser(
    description='Identifica hubs em um grafo, simula sua remoção e analisa a robustez. Permite escolher entre o grafo geral e o LCC.'
  )

  parser.add_argument(
    '--gexf-path', type=str, required=True,
    help='O caminho para o arquivo GEXF de entrada do grafo (necessário para a topologia da rede).'
  )
  
  parser.add_argument(
    '--metrics-json-path', type=str, required=True,
    help='O caminho para o arquivo JSON de entrada com as métricas pré-calculadas.'
  )

  parser.add_argument(
    '--output-json-path', type=str, required=True,
    help='O caminho para o arquivo JSON de saída com os resultados da análise.'
  )

  parser.add_argument(
    '--metric', type=str, default='degree', choices=['degree', 'betweenness', 'eigenvector', 'closeness'],
    help='A métrica de centralidade para identificar os hubs.'
  )

  parser.add_argument(
    '--num-hubs', type=int, default=20,
    help='O número de hubs a serem removidos no teste.'
  )
  
  parser.add_argument(
    '--lcc-only',
    action='store_true',  
    help='Se especificado, a análise de hubs será restrita ao Maior Componente Conectado (LCC).'
  )

  args = parser.parse_args()

  try:
    print(f"Lendo o grafo de: {args.gexf_path}")
    graph = nx.read_gexf(args.gexf_path)
  except FileNotFoundError:
    print(f"Erro: Arquivo GEXF não encontrado em '{args.gexf_path}'")
    return
      
  try:
    print(f"Lendo as métricas pré-calculadas de: {args.metrics_json_path}")
    with open(args.metrics_json_path, 'r', encoding='utf-8') as f:
      metrics_data = json.load(f)
  except FileNotFoundError:
    print(f"Erro: Arquivo JSON de métricas não encontrado em '{args.metrics_json_path}'")
    return
  except json.JSONDecodeError:
    print(f"Erro: Falha ao decodificar o arquivo JSON de métricas.")
    return

  metric_key_map = {
    'degree': 'degrees', 'betweenness': 'betweenness_centrality',
    'closeness': 'closeness_centrality', 'eigenvector': 'eigenvector_centrality'
  }
  selected_metric_key = metric_key_map.get(args.metric)

  if not selected_metric_key or selected_metric_key not in metrics_data:
    print(f"Erro: A métrica '{selected_metric_key}' não foi encontrada no arquivo JSON.")
    return

  centrality_dict = metrics_data[selected_metric_key]
  
  hubs_id_source_dict = centrality_dict
  analysis_scope = "General Graph"

  if args.lcc_only:
    print("\nOpção --lcc-only ativada. A análise será restrita ao LCC.")
    analysis_scope = "Largest Connected Component (LCC)"
    
    print("Identificando o Maior Componente Conectado (LCC)...")
    if nx.is_connected(graph):
      lcc_nodes = set(graph.nodes())
      print("O grafo já é totalmente conectado.")
    else:
      largest_component = max(nx.connected_components(graph), key=len)
      lcc_nodes = set(largest_component)
      print(f"LCC identificado com {len(lcc_nodes)} nós (de um total de {graph.number_of_nodes()}).")

    print(f"Filtrando a métrica '{selected_metric_key}' para conter apenas os nós do LCC...")
    lcc_centrality_dict = {
      node: centrality for node, centrality in centrality_dict.items() if node in lcc_nodes
    }

    if not lcc_centrality_dict:
      print("Erro: Nenhum nó do LCC foi encontrado no dicionário de centralidades.")
      return
    
    hubs_id_source_dict = lcc_centrality_dict
  else:
    print("\nAnálise será executada nos vértices gerais do grafo (comportamento padrão).")

  print(f"\nIniciando análise de robustez com a remoção dos {args.num_hubs} principais hubs pela métrica de '{args.metric}'.")
  print(f"Escopo da identificação dos hubs: {analysis_scope}")
  
  hubs_to_remove = identify_hubs(hubs_id_source_dict, top_n=args.num_hubs)
  print(f"Principais hubs identificados: {hubs_to_remove}")

  attack_results = analyze_network_attack(graph, hubs_to_remove)
  attack_results['hubs_removed_info'] = {
    'metric_used': args.metric,
    'source_metric_key': selected_metric_key,
    'analysis_scope': analysis_scope, # Registra o escopo no resultado
    'hubs_ids': hubs_to_remove
  }

  try:
    output_dir = os.path.dirname(args.output_json_path)
    if output_dir and not os.path.exists(output_dir):
      os.makedirs(output_dir)

    with open(args.output_json_path, 'w', encoding='utf-8') as f:
      json.dump(attack_results, f, ensure_ascii=False, indent=4)
    
    print(f"\nAnálise de robustez concluída. Resultados salvos em: {args.output_json_path}")
    print(f"Redução no tamanho do maior componente conectado: {attack_results['impact']['lcc_size_reduction_percent']:.2f}%")

  except IOError as e:
    print(f"Erro ao salvar o arquivo JSON de saída: {e}")

if __name__ == '__main__':
  main()