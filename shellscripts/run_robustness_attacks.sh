CONDA_ENV_NAME="networks_tocantins"

# Define os caminhos base
BASE_GRAPH_DIR="results/graphs"
BASE_METRICS_DIR="results/metrics"
BASE_ATTACK_DIR="results/attack"

# Lista de instituições (ajuste conforme necessário)
institutions=("tocantins" "uft" "ifto" "unitins" "ceulp" "ufnt") # Adicione outras instituições aqui se houver

start_year=2024
end_year=2024

# Métricas de centralidade a serem testadas
metrics=("degree" "betweenness" "eigenvector" "closeness")

# Número de hubs a serem removidos
num_hubs_range=$(seq 10 20 70)

# Verifica se o Conda está disponível
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

echo "Ambiente $CONDA_ENV_NAME ativado."

echo "Iniciando a análise de robustez para várias instituições, anos, métricas e número de hubs..."
echo "--------------------------------------------------------"

# Loop pelas instituições
for institution in "${institutions[@]}"; do
  echo "Processando instituição: $institution"

  # Loop pelos anos
  for year in $(seq $start_year $end_year); do
    echo "  Processando ano: $year"

    gexf_path="${BASE_GRAPH_DIR}/${institution}/graph_${institution}_${year}.gexf"
    metrics_json_path="${BASE_METRICS_DIR}/${institution}/${institution}_${year}.json"

    # Verifica se os arquivos de entrada existem
    if [ ! -f "$gexf_path" ]; then
      echo "    Aviso: Arquivo GEXF não encontrado para ${institution} - ${year} em: $gexf_path. Pulando."
      continue # Pula para a próxima iteração do loop de ano
    fi
    if [ ! -f "$metrics_json_path" ]; then
      echo "    Aviso: Arquivo JSON de métricas não encontrado para ${institution} - ${year} em: $metrics_json_path. Pulando."
      continue # Pula para a próxima iteração do loop de ano
    fi

    # Loop pelas métricas
    for metric in "${metrics[@]}"; do
      echo "    Testando métrica: $metric"

      # Loop pelo número de hubs a serem removidos
      for num_hubs in $num_hubs_range; do
        echo "      Testando remoção de ${num_hubs} hubs..."

        output_dir="${BASE_ATTACK_DIR}/${institution}"
        output_json_path="${output_dir}/${institution}_attack_${year}_${metric}_${num_hubs}.json"

        # Cria o diretório de saída se não existir
        mkdir -p "$output_dir"

        echo "        Executando hub_robustness_analyzer.py para ${institution} - ${year} - ${metric} - ${num_hubs} hubs..."

        # Executa o script hub_robustness_analyzer.py
        python scripts/hub_robustness_analyzer.py \
          --gexf-path "$gexf_path" \
          --metrics-json-path "$metrics_json_path" \
          --output-json-path "$output_json_path" \
          --metric "$metric" \
          --num-hubs "$num_hubs" \
          --lcc-only # Adicione ou remova esta flag conforme sua necessidade

        if [ $? -eq 0 ]; then
          echo "        Análise para ${institution} - ${year} - ${metric} - ${num_hubs} hubs concluída com sucesso."
        else
          echo "        Erro na análise para ${institution} - ${year} - ${metric} - ${num_hubs} hubs. Verifique o log acima."
        fi
        echo "" # Linha em branco para melhor legibilidade entre os ataques
      done
    done
  done
  echo "--------------------------------------------------------"
done

echo "Todas as análises de robustez foram concluídas."