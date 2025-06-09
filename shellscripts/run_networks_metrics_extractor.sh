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

institutions=("tocantins")

start_year=2023
end_year=2024

echo "Iniciando a análise de rede para várias instituições e anos..."
echo "--------------------------------------------------------"

# Loop pelas instituições
for institution in "${institutions[@]}"; do
  echo "Processando instituição: $institution"
  
  # Loop pelos anos
  for year in $(seq $start_year $end_year); do
    echo "  Processando ano: $year"

    # Define os caminhos de entrada e saída para o grafo GEXF e as métricas JSON
    gexf_path="results/graphs/${institution}/graph_${institution}_${year}.gexf"
    output_json_path="results/metrics/${institution}/${institution}_${year}.json"
    
    # Verifica se o arquivo GEXF existe antes de tentar processá-lo
    if [ -f "$gexf_path" ]; then
      echo "    Executando network_metrics_extractor.py para ${institution} - ${year}..."
      
      # Executa o script network_metrics_extractor.py com os caminhos definidos
      # Certifique-se de que o caminho para network_metrics_extractor.py está correto
      python scripts/network_metrics_extractor.py --gexf-path "$gexf_path" --output-json-path "$output_json_path"
      
      if [ $? -eq 0 ]; then
        echo "    Análise para ${institution} - ${year} concluída com sucesso."
      else
        echo "    Erro na análise para ${institution} - ${year}. Verifique o log acima."
      fi
    else
      echo "    Aviso: Arquivo GEXF não encontrado para ${institution} - ${year} em: $gexf_path. Pulando."
    fi
    echo "" # Linha em branco para melhor legibilidade
  done
  echo "--------------------------------------------------------"
done

echo "Todas as análises foram concluídas."
