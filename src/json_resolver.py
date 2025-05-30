import ast

def json_string_to_dict(string_input) -> dict:
  """
  Converte uma string que se parece com um dicionário Python ou JSON
  em um dicionário Python.

  Args:
    string_input: A string contendo o código que se assemelha a um dicionário ou JSON.

  Returns:
    Um dicionário Python.
  """
  string_processada = string_input.replace('\u2013', '-')
  try:
    result = ast.literal_eval(string_processada)

    if not isinstance(result, dict):
      raise ValueError("A string não representa um dicionário válido. Tipo retornado: {}".format(type(result).__name__))
    
    return result
  except (ValueError, SyntaxError) as e:
    print(f"Erro ao codificar a string '{string_input}': {e}")
  