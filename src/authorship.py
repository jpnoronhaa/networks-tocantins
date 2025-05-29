import pandas as pd
import json


def extract_authors(df: pd.DataFrame) -> set:
  """
  Extrai informações de autores de um DataFrame e retorna um set de autores únicos.

  Args:
    df (pd.DataFrame): O DataFrame contendo os dados dos trabalhos.

  Returns:
    set: Um set de dicionários, onde cada dicionário representa um autor único.
      Cada dicionário contém as seguintes chaves (se disponíveis):
      - 'id': ID do autor (authorships.author.id)
      - 'display_name': Nome de exibição do autor (authorships.author.display_name)
      - 'orcid': ORCID do autor (authorships.author.orcid)
      - 'country': Países do autor (authorships.countries)
      - 'raw_author_name': Nome bruto do autor (authorships.raw_author_name)
      - 'institution': Lista de dicionários com 'id', 'display_name' e 'country_code' da instituição
      - 'affiliation': Lista de dicionários com 'raw_affiliation_string' e 'institution_ids' da afiliação
  """
  authors_set = set()

  # Mapeamento das colunas para facilitar o acesso
  author_columns = {
    'raw_author_name': 'authorships.raw_author_name',
    'raw_affiliation_strings': 'authorships.raw_affiliation_strings',
    'author_id': 'authorships.author.id',
    'display_name': 'authorships.author.display_name',
    'orcid': 'authorships.author.orcid',
    'countries': 'authorships.countries',
    'institutions': 'authorships.institutions'
  }

  for _, row in df.iterrows():
    # Dividir as strings por '|' para obter as informações de cada autor
    # Usamos .get() com um valor padrão de '' para evitar KeyError se a coluna não existir
    # e .split('|') para transformar a string em uma lista, ou uma lista vazia se for None
    raw_names = row.get(author_columns['raw_author_name'], '').split('|') if pd.notna(row.get(author_columns['raw_author_name'])) else []
    affiliation_strings = row.get(author_columns['raw_affiliation_strings'], '').split('|') if pd.notna(row.get(author_columns['raw_affiliation_strings'])) else []
    author_ids = row.get(author_columns['author_id'], '').split('|') if pd.notna(row.get(author_columns['author_id'])) else []
    display_names = row.get(author_columns['display_name'], '').split('|') if pd.notna(row.get(author_columns['display_name'])) else []
    orcids = row.get(author_columns['orcid'], '').split('|') if pd.notna(row.get(author_columns['orcid'])) else []
    countries = row.get(author_columns['countries'], '').split('|') if pd.notna(row.get(author_columns['countries'])) else []
    institutions_raw = row.get(author_columns['institutions'], '').split('|') if pd.notna(row.get(author_columns['institutions'])) else []

    # Determinar o número máximo de autores para iterar
    num_authors = max(len(raw_names), len(affiliation_strings), len(author_ids),
    len(display_names), len(orcids), len(countries), len(institutions_raw))

    for i in range(num_authors):
      author_info = {}

      author_id = author_ids[i] if i < len(author_ids) and pd.notna(author_ids[i]) and author_ids[i] != 'None' else None

      # Se não houver um ID de autor válido, não podemos garantir a unicidade, então pulamos
      if not author_id:
        continue

      author_info['id'] = author_id

      if i < len(display_names) and pd.notna(display_names[i]) and display_names[i] != 'None':
        author_info['display_name'] = display_names[i]
      if i < len(orcids) and pd.notna(orcids[i]) and orcids[i] != 'None':
        author_info['orcid'] = orcids[i]
      if i < len(countries) and pd.notna(countries[i]) and countries[i] != 'None':
        author_info['country'] = countries[i]
      if i < len(raw_names) and pd.notna(raw_names[i]) and raw_names[i] != 'None':
        author_info['raw_author_name'] = raw_names[i]

      # Processar instituições
      if i < len(institutions_raw) and pd.notna(institutions_raw[i]) and institutions_raw[i] != 'None':
        inst_str = institutions_raw[i].strip() # Remover espaços em branco extras
        if inst_str and inst_str != 'None': # Checa se a string não está vazia ou é 'None'
          try:
            # Substitui aspas simples por duplas e tenta carregar como JSON
            institution = json.loads(inst_str.replace("'", "\"").strip())
            
            if 'id' in institution:
              author_info['institution_id'] = institution['id']
            if 'display_name' in institution:
              author_info['institution_display_name'] = institution['display_name']
            if 'country_code' in institution:
              author_info['institution_country_code'] = institution['country_code']
              
          except json.JSONDecodeError as e:
            # Opcional: logar erros de parsing para depuração
            print(f"Erro ao parsear instituição '{inst_str}': {e}")
            pass
        else: # Opcional: logar se a string de instituição for vazia/None
          print(f"Aviso: String de instituição vazia/None: '{inst_str}'")
          pass

      # Processar afiliações
      # author_affiliations = []
      # if i < len(affiliation_strings_list) and pd.notna(affiliation_strings_list[i]) and affiliation_strings_list[i] != 'None':
      #     aff_str = affiliation_strings_list[i].strip() # Remover espaços em branco extras
      #     if aff_str and aff_str != 'None': # Checa se a string não está vazia ou é 'None'
      #         try:
      #             if aff_str.startswith('{') and aff_str.endswith('}'):
      #                 affiliation_list = [json.loads(aff_str.replace("'", "\""))]
      #             else:
      #                 affiliation_list = json.loads(aff_str.replace("'", "\""))

      #             if not isinstance(affiliation_list, list):
      #                 affiliation_list = [affiliation_list]

      #             for aff in affiliation_list:
      #                 if isinstance(aff, dict): # Garante que 'aff' é um dicionário
      #                     aff_data = {}
      #                     if 'raw_affiliation_string' in aff:
      #                         aff_data['raw_affiliation_string'] = aff['raw_affiliation_string']
      #                     if 'institution_ids' in aff:
      #                         aff_data['institution_ids'] = aff['institution_ids']
      #                     if aff_data:
      #                         author_affiliations.append(aff_data)
      #                 # else: # Opcional: logar caso 'aff' não seja um dict
      #                 #     print(f"Aviso: Elemento inesperado em affiliation_strings: {aff}")
      #         except json.JSONDecodeError as e:
      #             # print(f"Erro ao parsear afiliação '{aff_str}': {e}")
      #             pass
      #     else: # Opcional: logar se a string de afiliação for vazia/None
      #         # print(f"Aviso: String de afiliação vazia/None: '{aff_str}'")
      #         pass
      # if author_affiliations:
      #     author_info['affiliations'] = author_affiliations

      # Adicionar o autor ao set. Usamos o ID do autor para garantir a unicidade.
      # Convertemos o dicionário para uma tupla de itens para que seja "hashable" e possa ser adicionado a um set.
      # Isso garante que autores com o mesmo ID (e outras informações) não sejam duplicados.
      authors_set.add(frozenset(author_info.items()))

  # Converter de volta para um set de dicionários (se necessário para uso posterior)
  # ou manter como frozenset para garantir a unicidade pelo ID.
  # Para o propósito de "set com a lista de autores", o frozenset é mais adequado.
  # Se precisar de um set de dicionários para manipular, a linha abaixo pode ser usada:
  # return {dict(item) for item in authors_set}
  return authors_set