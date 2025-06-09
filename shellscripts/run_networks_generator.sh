CONDA_ENV_NAME="networks_tocantins"

DATA_DIR="data"

PYTHON_SCRIPT="scripts/network_generator.py"

OUTPUT_GEXF_BASE_DIR="results/graphs"

DEFAULT_FILE_SUFFIX="geral"

START_YEAR=1998
END_YEAR=2024

if ! command -v conda &> /dev/null
then
  echo "Erro: Conda não encontrado. Por favor, certifique-se de que o Conda esteja instalado e no seu PATH."
  exit 1
fi

echo "Ativando o ambiente Conda: $CONDA_ENV_NAME..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV_NAME"

if [ $? -ne 0 ]; then
  echo "Erro: Não foi possível ativar o ambiente Conda '$CONDA_ENV_NAME'. Verifique se ele existe."
  exit 1
fi

echo "Verificando e instalando o pacote 'src'..."
pip install -e .

if [ $? -ne 0 ]; then
  echo "Erro: Falha ao instalar o pacote 'src' com 'pip install -e .'."
  exit 1
fi

echo "Ambiente '$CONDA_ENV_NAME' ativado e 'src' instalado com sucesso."


echo "Iniciando a geração dos grafos de coautoria para múltiplos arquivos..."

for works_csv_path in "$DATA_DIR"/works_*.csv; do
  if [ -f "$works_csv_path" ]; then
    echo "----------------------------------------------------"
    echo "Processando arquivos relacionados a: $works_csv_path"

    filename=$(basename -- "$works_csv_path")
    file_prefix="${filename%.*}"
    file_suffix="${file_prefix#works_}"

    authors_csv_path="$DATA_DIR/authors_${file_suffix}.csv"

    if [ ! -f "$authors_csv_path" ]; then
      echo "Aviso: Arquivo de autores '$authors_csv_path' não encontrado para '$works_csv_path'. Pulando..."
      continue
    fi
    
    CURRENT_OUTPUT_GEXF_DIR="$OUTPUT_GEXF_BASE_DIR/$file_suffix"

    echo "Usando o sufixo de arquivo: $file_suffix"
    echo "Caminho de saída GEXF: $CURRENT_OUTPUT_GEXF_DIR"
    echo "Arquivo de trabalhos: $works_csv_path"
    echo "Arquivo de autores: $authors_csv_path"

    python "$PYTHON_SCRIPT" \
      --csv-path-works "$works_csv_path" \
      --csv-path-authors "$authors_csv_path" \
      --output-gexf-path "$CURRENT_OUTPUT_GEXF_DIR/" \
      --file-suffix "$file_suffix" \
      --start-year "$START_YEAR" \
      --end-year "$END_YEAR"

    if [ $? -ne 0 ]; then
      echo "Erro ao processar $works_csv_path e $authors_csv_path. O script Python retornou um erro."
    else
      echo "Concluído para $works_csv_path e $authors_csv_path. Grafos GEXF salvos em: $CURRENT_OUTPUT_GEXF_DIR"
    fi
  fi
done

echo "----------------------------------------------------"
echo "Todos os arquivos foram processados ou tentados."
echo "Desativando o ambiente Conda..."
conda deactivate

echo "Script concluído."