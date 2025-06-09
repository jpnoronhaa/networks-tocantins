import pandas as pd
from src.json_resolver import json_string_to_dict

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
  """
  authors_set = set()
  authors_ids = set()

  author_columns = {
    'raw_author_name': 'authorships.raw_author_name',
    'author_id': 'authorships.author.id',
    'display_name': 'authorships.author.display_name',
    'orcid': 'authorships.author.orcid',
    'countries': 'authorships.countries',
    'institutions': 'authorships.institutions'
  }

  for _, row in df.iterrows():
    raw_names = row.get(author_columns['raw_author_name'], '').split('|') if pd.notna(row.get(author_columns['raw_author_name'])) else []
    author_ids = row.get(author_columns['author_id'], '').split('|') if pd.notna(row.get(author_columns['author_id'])) else []
    display_names = row.get(author_columns['display_name'], '').split('|') if pd.notna(row.get(author_columns['display_name'])) else []
    orcids = row.get(author_columns['orcid'], '').split('|') if pd.notna(row.get(author_columns['orcid'])) else []
    countries = row.get(author_columns['countries'], '').split('|') if pd.notna(row.get(author_columns['countries'])) else []
    institutions_raw = row.get(author_columns['institutions'], '').split('|') if pd.notna(row.get(author_columns['institutions'])) else []

    num_authors = max(len(raw_names), len(author_ids),
    len(display_names), len(orcids), len(countries), len(institutions_raw))

    for i in range(num_authors):
      author_info = {}

      author_id = author_ids[i] if i < len(author_ids) and pd.notna(author_ids[i]) and author_ids[i] != 'None' else None

      if not author_id or author_id in authors_ids:
        continue
      authors_ids.add(author_id)
      author_info['id'] = author_id

      if i < len(display_names) and pd.notna(display_names[i]) and display_names[i] != 'None':
        author_info['display_name'] = display_names[i]
      if i < len(orcids) and pd.notna(orcids[i]) and orcids[i] != 'None':
        author_info['orcid'] = orcids[i]
      if i < len(countries) and pd.notna(countries[i]) and countries[i] != 'None':
        author_info['country'] = countries[i]
      if i < len(raw_names) and pd.notna(raw_names[i]) and raw_names[i] != 'None':
        author_info['raw_author_name'] = raw_names[i]

      if i < len(institutions_raw) and pd.notna(institutions_raw[i]) and institutions_raw[i] != 'None':
        inst_str = institutions_raw[i].strip()
        if inst_str and inst_str != 'None':
          institution = json_string_to_dict(inst_str)
          
          if 'id' in institution:
            author_info['institution_id'] = institution['id']
          if 'display_name' in institution:
            author_info['institution_display_name'] = institution['display_name']
          if 'country_code' in institution:
            author_info['institution_country_code'] = institution['country_code']

      authors_set.add(frozenset(author_info.items()))

  return authors_set

def extract_authors_ids(df: pd.DataFrame) -> set:
  """
  Extrai os IDS de autores de um DataFrame e retorna um set de autores únicos.

  Args:
    df (pd.DataFrame): O DataFrame contendo os dados dos trabalhos.

  Returns:
    set: Um set de ids.
  """
  authors_set_ids = set()

  for _, row in df.iterrows():
    authors_ids = row.get('authorships.author.id', '').split('|') if pd.notna(row.get('authorships.author.id')) else []
    authors_set_ids.update(authors_ids)

  return authors_set_ids