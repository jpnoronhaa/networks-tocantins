# Extração de Autores

O script `scripts/authors_extractor.py` analisa um arquivo CSV, extrai os autores do arquivo e gera um CSV como saída.

Para extrair os autores de uma base de dados basta rodar o comando:

```bash
$ python scripts/authors_extractor.py --csv-path <ARQUIVO_DE_ENTRADA_CSV> --output-csv-path <ARQUIVO_DE_SAIDA_CSV>
```