# networks-tocantins


O arquivo `environment.yml` possui as configurações do ambiente conda, ele é funcional para diferentes plataformas (MacOS e Linux preferencialmente).

Para criar um novo ambiente conda com as bibliotecas utilizadas pelo projeto basta usar o comando:

```bash
$ conda env create -f environment.yml
```

## Instalação do módulo `src/`

Para instalar o módulo basta rodar no terminal no diretório raiz:

```bash
$ pip install -e .
```

## Documentação do código

Na pasta `docs/` estão os arquivos `.md` que documentam as principais funcionalidades do código.


## Como fazer download dos dados brutos

Para fazer download dos arquivos de dados brutos basta acessar o site oficial do OpenAlex, selecionar a instituição, selecionar a filtragem por anos (1998 - 2024) e exportar os trabalhos como arquivo CSV.

Abaixo estão os links para acessar os dados pelo site e pela API.

- IFTO

  Site: [https://openalex.org/works?page=1&filter=authorships.institutions.lineage%3Ai4210139493,publication_year%3A1998%20-%202024](https://openalex.org/works?page=1&filter=authorships.institutions.lineage%3Ai4210139493,publication_year%3A1998%20-%202024)

  API: [https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i4210139493,publication_year:1998+-+2024&sort=cited_by_count:desc&per_page=10](https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i4210139493,publication_year:1998+-+2024&sort=cited_by_count:desc&per_page=10)

- Unitins

  Site: [https://openalex.org/works?page=1&filter=authorships.institutions.lineage%3Ai4210089573,publication_year%3A1998%20-%202024&view=list,api,report](https://openalex.org/works?page=1&filter=authorships.institutions.lineage%3Ai4210089573,publication_year%3A1998%20-%202024&view=list,api,report)

  API: [https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i4210089573,publication_year:1998+-+2024&sort=cited_by_count:desc&per_page=10](https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i4210089573,publication_year:1998+-+2024&sort=cited_by_count:desc&per_page=10)
    
- UFT

  Site: [https://openalex.org/works?page=1&filter=authorships.institutions.lineage%3Ai41458283,publication_year%3A1998%20-%202024&view=list,report,api](https://openalex.org/works?page=1&filter=authorships.institutions.lineage%3Ai41458283,publication_year%3A1998%20-%202024&view=list,report,api)

  API: [https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i41458283,publication_year:1998+-+2024&sort=cited_by_count:desc&per_page=10](https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i41458283,publication_year:1998+-+2024&sort=cited_by_count:desc&per_page=10)


Para que o código funcione normalmente os arquivos devem estar contidos na pasta `/data`.