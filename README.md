# Pipeline Bioinformática

Autor : Ed Carlos Santos e Silva

O seguinte projeto foi desenvolvido para atender ao processo seletivo de Bioinformata 

Objetivo:
0. Conversão do arquivo cram;  
1. Cálculo de cobertura genômica;
2. Inferência do sexo genético a partir dos dados de sequenciamento;
3. Estimativa de contaminação por DNA exógeno ou de outros indivíduos.

# Estrutura do projto



# Instalação

- 1 - Ferramentas

Samtools
Bcftools

Use o código

sudo apt-get install samtools bcftools

- 2 - Linguagens

Python 3.10.12

- 3 - Clonar o projeto

git clone ...

- 4 - Instalar dependências

python -m venv bioinformatics_venv
source bioinformatics_venv/bin/activate
pip install -r requirements.txt

- 5 - Baixar arquivos

Carregue os arquivos para processamento nas respectivas pastas

crai_files
-- Carregue o arquivo CRAI 

cram_files
-- Carregue o arquivo CRAM 

bed_files
-- Carregue o arquivo BED 
hg38_exome_v2.0.2_targets_sorted_validated.re_annotated.bed

ref_gen files
-- Carregue o arquivo FASTA do genoma de referência
GRCh38_full_analysis_set_plus_decoy_hla.fa do (https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/)

* OBSERVAÇÃO : Certifique-se de que os arquivos CRAI e CRAM tenham o mesmo nome e verifique a integridade do download

# Uso

- No terminal, posicionado na pasta do projeto ative a env e execute o arquivo do pipeline 

source bioinformatics_venv/bin/activate

- Execute o script

python qc_pipeline.py

# Resultados e Relatóriaos

- Todos os relatórios estarão na pasta output separados em: 

logs 
Na pasta logs será gerado o arquivo pipeline.log com o histórico geral das etapas realizadas pelo pipeline

Será gerada uma pasta com o nome da amostra , contendo: 

-- Os arquivos

coverage_results.txt
sex_inference.txt

-- Pasta de logs da amostra

reports

# Implementações futuras

- Container
- Interface gráfica 
