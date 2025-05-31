CONDA_ENV_NAME="networks_tocantins"

DATA_DIR="data"

PYTHON_SCRIPT="scripts/authors_extractor.py"

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

echo "Ambiente $CONDA_ENV_NAME ativado e 'src' instalado."


echo "Iniciando a extração de autores para múltiplos arquivos..."

for input_csv in "$DATA_DIR"/works_*.csv; do
    if [ -f "$input_csv" ]; then
        echo "Processando: $input_csv"

        filename=$(basename -- "$input_csv")
        filename_no_ext="${filename%.*}"

        output_csv="$DATA_DIR/authors_${filename_no_ext#works_}.csv"

        python "$PYTHON_SCRIPT" --csv-path "$input_csv" --output-csv-path "$output_csv"

        if [ $? -ne 0 ]; then
            echo "Erro ao processar $input_csv. O script Python retornou um erro."
        else
            echo "Concluído para $input_csv. Saída em: $output_csv"
        fi
        echo "----------------------------------------------------"
    fi
done

echo "Todos os arquivos foram processados ou tentados."
echo "Desativando o ambiente Conda..."
conda deactivate

echo "Script concluído."