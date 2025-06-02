import pandas as pd

def count_papers_by_year(df, start_year, end_year):
  """
  Calcula o número de trabalhos para cada ano dentro de um intervalo especificado.

  Args:
    df (pd.DataFrame): O DataFrame de entrada com uma coluna 'publication_year'.
    start_year (int): O ano de início do intervalo (inclusive).
    end_year (int): O ano de término do intervalo (inclusive).

  Returns:
    dict: Um dicionário onde as chaves são os anos e os valores são a contagem de
    trabalhos publicados naquele ano dentro do intervalo especificado. Anos
    dentro do intervalo que não possuem trabalhos terão uma contagem de 0.
  """

  year_counts = {year: 0 for year in range(start_year, end_year + 1)}

  for year in df['publication_year']:
    if pd.isna(year):
      continue
    try:
      year_int = int(year)
    except ValueError:
      continue
    
    if start_year <= year_int <= end_year:
      year_counts[year_int] += 1
          
  return year_counts