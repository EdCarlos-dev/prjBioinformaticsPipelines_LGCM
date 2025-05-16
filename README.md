# 🧬 Pipeline de Controle de Qualidade de Exoma (WES) - Bioinformática

O seguinte projeto foi desenvolvido para atender ao processo seletivo de Bioinformata 

## 1. 👤 Identificação

**Autor:** Ed Carlos Santos e Silva  
**Email:** edcarlos.biomedic@gmail.com  

---

## 2. 🧾 Descrição do Pipeline


Este pipeline realiza o controle de qualidade de dados de sequenciamento do exoma humano (WES), a partir de arquivos CRAM. As principais etapas são:

- Conversão de arquivos `.cram` para `.bam`
- Indexação dos arquivos BAM
- Cálculo da cobertura com base em arquivo BED
- Inferência do sexo genético (baseada na cobertura dos cromossomos X e Y)
- Estimativa de contaminação (em implementação)
- Geração de relatórios por amostra

---

## Estrutura do projeto

<img src="">


## 3. 🛠️ Instruções de Uso

### 3.0. Baixando as Ferramentas e Dependências

Python 3.10.12

samtools

bcftools

VerifyBamID - https://genome.sph.umich.edu/wiki/VerifyBamID

- Instalação

Use o código

```
bash
sudo apt-get install samtools bcftools
```




### 3.1. Clonando o repositório

```
bash
git clone https://github.com/seuusuario/repo.git
cd repo

```

### 3.2. Criando o Ambiente Virtual

* posicionado na pasta do projeto

```
python -m venv bioinformatics_venv
source bioinformatics_venv/bin/activate
pip install -r requirements.txt
```

### 3.3. Estrutura Esperada de Diretórios de dados

```
data/
├── input/
│   ├── bed_files/         # Arquivo BED com regiões de interesse
│   ├── crai_files/        # Arquivos .crai
│   ├── cram_files/        # Arquivos .cram
│   └── ref_gen_files/     # Genoma de referência (.fa e .fai)
├── intermediate/          # BAMs e arquivos intermediários
└── output/                # Relatórios finais e gráficos
```

### 3.4. Carregando os arquivos


Carregue os arquivos para processamento nas respectivas pastas

crai_files
-- Carregue o arquivo CRAI que serão processados

cram_files
-- Carregue os arquivos CRAM que serão processados

bed_files
-- Carregue o arquivo BED 
hg38_exome_v2.0.2_targets_sorted_validated.re_annotated.bed

ref_gen files
-- Carregue o arquivo FASTA do genoma de referência
GRCh38_full_analysis_set_plus_decoy_hla.fa 
Fonte - (https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/)

```
bash
wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa
```


* OBSERVAÇÃO 1 : Certifique-se de alterar em dev/apps/.env os nomes dos arquivos que deseja usar como .bed e .fa

--- O script concatena o caminho da pasta com o nome na env, 

--- assim é possível ter mais de um arquivo bed já carregados na pasta data/bed_files/ e usá-los conforme a necessidade 

* OBSERVAÇÃO 2 : Certifique-se de que os arquivos CRAI e CRAM tenham o mesmo nome e verifique a integridade do download

* OBSERVAÇÃO 3 : O Script foi estruturado para iterar em todos os arquivos  .cram existentes na parta data/cram_files/ gerando os respectivos .bam e .bai para análise e caso o script seja interrompido no meio do processo ele não fará a extração do  cram - BAM já realizada. Caso haja um erro e o último .bam gerado estejá corrompido , a sugestão é que o mesmo seja apagado para retomar o processo.


- Para a verificação da contaminação usei os arquivos vcf desse site (é possível baixar separadamente por cromossomo o script contaminatio.py vai concatenar usando o bcftools, logo é possível usar todos ou apenas doi como desejado)
--- https://www.ebi.ac.uk/ena/browser/view/PRJEB30460


### 3.6. Executando o Pipeline

- No terminal, posicionado na pasta pathdoprojeto/dev/apps do projeto ative a env e execute o arquivo do pipeline 

```
python pipeline.py
```

## 4 📦 Dependências e Ferramentas

Python 3.10.12

samtools

bcftools


## 5. 💻 Comandos de Exemplo

- Para o uso da estrutura de pastas e arquivos de configuração já existentes

bash
```
python pipeline.py
```

- Aqui temos um modo de usar o pipeline usando argumentos presentes no script , onde é possível apontar para um path ou arquivos diferentes para uso

bash
```
python pipeline.py \
  --cram_dir data/input/cram_files \
  --bed data/input/bed_files/meu_exoma.bed \
  --ref_fasta data/input/ref_gen_files/GRCh38.fa \
  --intermediate_dir data/intermediate \
  --output_dir data/output 
  
```



## 6. 📂 Explicação dos Outputs
Para cada amostra processada, será criada uma pasta:

bash
```
data/output/reports/NOME_DA_AMOSTRA/
├── coverage_nome_da_amostra_results.txt   # Métricas de cobertura
├── coverage_nome_da_amostra_results.png   # Histograma de cobertura
├── sex_inference_nome_da_amostra.txt      # Resultado da inferência de sexo
├── logs/                                  # Logs detalhados por amostra
```

Exemplos de métricas:
Profundidade média

% de regiões cobertas ≥ 10x e ≥ 30x

Cobertura dos cromossomos X e Y

Sexo genético estimado


## 7. 📊 Resultados obtidos

- Para a amostra solicitada no teste esses são os resultados parciais obtidos

cobertura mantive os txts completos na pasta output

Profundidade Média: 67738.44x

% Coberto >= 10x: 97.27%

% Coberto >= 30x: 96.84%


Sexo

Cromossomo X Cobertura: 62.88x

Cromossomo Y Cobertura: 90.12x

Sexo Predito: Masculino


### 7.1.Saídas de log esperadas

* outputs/logs/pipeline.log

```
2025-05-15 17:56:16,834 - INFO - Início do pipeline de controle de qualidade para múltiplos arquivos
2025-05-15 17:56:16,836 - INFO - Iniciando processamento da amostra: [Nome_Amostra]
2025-05-15 17:56:16,836 - INFO - Executando: Conversão de CRAM para BAM: /diretorioprojeto/data/input/cram_files/[Nome_Amostra].cram -> /diretorioprojeto/data/intermediate/bam_files/[Nome_Amostra].bam
2025-05-15 18:00:46,130 - INFO - CRAM convertido para BAM: /diretorioprojeto/data/intermediate/bam_files/[Nome_Amostra].bam
2025-05-15 18:01:11,658 - INFO - Arquivo BAM indexado: /diretorioprojeto/data/intermediate/bam_files/[Nome_Amostra].bam.bai
2025-05-15 18:03:07,253 - INFO - Cobertura calculada e salva em /diretorioprojeto/data/output/reports/[Nome_Amostra]/coverage_[Nome_Amostra]_results.txt
2025-05-15 18:03:07,660 - INFO - Histograma de cobertura gerado e salvo em /diretorioprojeto/data/output/reports/[Nome_Amostra]/coverage_[Nome_Amostra]_results.png
2025-05-15 18:03:10,639 - INFO - Cobertura do cromossomo X: Valor x
2025-05-15 18:03:10,914 - INFO - Cobertura do cromossomo Y: Valor x
2025-05-15 18:03:10,915 - INFO - Sexo genético inferido e salvo em /diretorioprojeto/data/output/reports/[Nome_Amostra]/sex_inference_[Nome_Amostra].txt
2025-05-15 18:03:10,915 - INFO - Processamento da amostra [Nome_Amostra] concluído
2025-05-15 18:03:10,935 - INFO - Pipeline de controle de qualidade para múltiplos arquivos concluído

``` 

* output/reports/NOME_DA_AMOSTRA/logs/NomedaAmostra.log

```
2025-05-15 17:56:16,836 - INFO - Iniciando processamento da amostra: [Nome_Amostra]
2025-05-15 18:01:11,658 - INFO - Arquivo BAM indexado: /path/projeto/data/intermediate/bam_files/[Nome_Amostra].bam.bai
2025-05-15 18:03:07,253 - INFO - Cobertura calculada e salva em /path/projeto/data/output/reports/[Nome_Amostra]/coverage_[Nome_Amostra]_results.txt
2025-05-15 18:03:07,660 - INFO - Histograma de cobertura gerado e salvo em /path/projeto/data/output/reports/[Nome_Amostra]/coverage_[Nome_Amostra]_results.png
2025-05-15 18:03:10,915 - INFO - Sexo genético inferido e salvo em /path/projeto/data/output/reports/[Nome_Amostra]/sex_inference_[Nome_Amostra].txt
2025-05-15 18:03:10,915 - INFO - Processamento da amostra [Nome_Amostra] concluído

```



## 8. 🚧 Em desenvolvimento

- Estimativa de contaminação com VerifyBamID

- Geração automática de relatórios PDF

- Integração com múltiplas amostras por lote

- Container

- Interface gráfica 

## 9. 🧪 Testado com:

CRAM de alta cobertura (~1.5 GB)

Genoma de referência GRCh38 (plus decoy HLA)

Arquivo BED com regiões de exoma clínico

## 10. 📬 Contato

Dúvidas ou sugestões? Entre em contato por email ou abra uma issue aqui no GitHub!