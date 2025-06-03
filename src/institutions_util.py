import pandas as pd
import re
from collections import defaultdict
from itertools import combinations
from src.json_resolver import json_string_to_dict

def parse_institutions_string(institutions_str):
  """
  Analisa uma string contendo dicionários de instituições e retorna um conjunto de nomes de exibição de instituições únicos.

  Args:
    institutions_str (str): Uma string contendo uma ou mais representações em string
    de dicionários de instituições. Cada dicionário deve
    incluir uma chave 'display_name'.

  Returns:
    set: Um conjunto de strings, onde cada string é o 'display_name' único de uma
    instituição extraída da string de entrada.
  """
  if institutions_str is None:
    return set()
  institutions_in_paper = set()
  matches = re.findall(r"\{[^}]+\}", institutions_str)
  
  for match_str in matches:
    inst_dict = json_string_to_dict(match_str)
    institutions_in_paper.add(inst_dict['display_name'])

  return institutions_in_paper


def count_institutions(df):
  """
  Calcula o número de trabalhos em que cada instituição está presente.

  Args:
    df (pd.DataFrame): O DataFrame de entrada com uma coluna 'authorships.institutions'.

  Returns:
    dict: Um dicionário onde as chaves são os nomes de exibição das instituições e os valores
    são a contagem de trabalhos em que elas estão presentes.
  """
  institution_counts = defaultdict(int)

  for _, row in df.iterrows():
    institutions_str = row['authorships.institutions']
    institutions_in_paper = parse_institutions_string(institutions_str)

    for institution_name in institutions_in_paper:
      institution_counts[institution_name] += 1

  return dict(institution_counts)


def analyze_institution_papers(df, target_institutions):
  """
  Analisa os trabalhos quanto à exclusividade de cada instituição alvo, à coocorrência de todas as instituições alvo
  e à coocorrência de todas as combinações de instituições alvo.

  Args:
    df (pd.DataFrame): O DataFrame de entrada com uma coluna 'authorships.institutions'.
    target_institutions (list): Uma lista de nomes de instituições a serem analisadas.

  Returns:
    dict: Um dicionário contendo:
    - 'exclusive_papers_per_institution': Um dicionário onde as chaves são os nomes de
    exibição das instituições da lista `target_institutions` e os valores são a contagem
    de trabalhos onde APENAS essa instituição específica (da lista `target_institutions`)
    está presente, e nenhuma outra instituição da mesma lista está presente.
    - 'all_present_papers': A contagem de trabalhos onde TODAS as instituições da lista
    `target_institutions` estão presentes.
    - 'combinations_present_papers': Um dicionário onde as chaves são tuplas de instituições
    (representando uma combinação) e os valores são a contagem de trabalhos onde TODAS
    as instituições dessa combinação estão presentes.
  """
  exclusive_papers_per_institution = defaultdict(int)
  all_present_papers_count = 0
  combinations_present_papers = defaultdict(int)

  target_institutions_set = set(target_institutions)

  all_target_combinations = []
  for i in range(2, len(target_institutions) + 1):
    all_target_combinations.extend(combinations(sorted(target_institutions), i))

  print('all')
  print(all_target_combinations)

  for _, row in df.iterrows():
    institutions_str = row['authorships.institutions']
    institutions_in_paper = parse_institutions_string(institutions_str)
    
    if target_institutions_set.issubset(institutions_in_paper):
      all_present_papers_count += 1

    for institution_name in target_institutions:
      if institution_name in institutions_in_paper:
        other_target_institutions_set = target_institutions_set - {institution_name}
        
        if other_target_institutions_set.isdisjoint(institutions_in_paper):
          exclusive_papers_per_institution[institution_name] += 1
          
    for combo in all_target_combinations:
      combo_set = set(combo)
      if combo_set.issubset(institutions_in_paper):
        combinations_present_papers[combo] += 1

  combinations_present_papers_str_keys = {
        ", ".join(combo): count
        for combo, count in combinations_present_papers.items()
    }   
  
  return {
    'exclusive_papers_per_institution': dict(exclusive_papers_per_institution),
    'all_present_papers': all_present_papers_count,
    'combinations_present_papers': combinations_present_papers_str_keys
  }