import pandas as pd
import numpy as np

def generate_variable_dictionary(df: pd.DataFrame) -> dict:
  """
  Gera um dicionário de variáveis a partir de um DataFrame do Pandas.

  Cada chave do dicionário representa o nome de uma variável (coluna do DataFrame),
  e o valor é outro dicionário contendo metadados sobre a variável.

  Args:
    df (pd.DataFrame): O DataFrame de entrada.

  Returns:
    dict: Um dicionário onde as chaves são os nomes das variáveis e os valores
      são dicionários com os seguintes metadados:
      - 'nome_da_variavel': Nome da coluna.
      - 'tipo': Tipo de dado inferido da coluna (e.g., 'int64', 'object').
      - 'descricao': Uma descrição genérica (a ser preenchida manualmente).
      - 'exemplo': Um valor de exemplo da coluna (primeiro valor não nulo).
      - 'quantidade_valores_nulos': Número de valores nulos na coluna.
      - 'observacao': Observações adicionais (a ser preenchida manualmente).
  """
  variable_dict = {}
  for column in df.columns:
      data_type = str(df[column].dtype)

      raw_example_value = df[column].dropna().iloc[0] if not df[column].dropna().empty else None

      if isinstance(raw_example_value, (np.integer, np.floating)):
        example_value = raw_example_value.item()
      elif isinstance(raw_example_value, np.bool_):
        example_value = bool(raw_example_value)
      else:
        example_value = raw_example_value

      null_count = int(df[column].isnull().sum())
      
      variable_dict[column] = {
          'nome_da_variavel': column,
          'tipo': data_type,
          'descricao': 'DESCRIÇÃO DA VARIÁVEL (a ser preenchida)',
          'exemplo': example_value,
          'quantidade_valores_nulos': null_count,
          'observacao': 'OBSERVAÇÃO (a ser preenchida, ex: "valores categóricos", "intervalo de 0 a 100")'
      }
  return variable_dict