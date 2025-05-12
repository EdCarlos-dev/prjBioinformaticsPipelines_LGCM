# Pipeline Bioinformática

Autor : Ed Carlos Santos e Silva

O seguinte projeto foi desenvolvido para atender ao processo seletivo de Bioinformata 

Objetivo:
0. Conversão do arquivo cram , foi utilizada a solução Samtools  
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
cram_files

bed_files
-- Carregue o arquivo 
hg38_exome_v2.0.2_targets_sorted_validated.re_annotated.bed

ref_gen files
-- Carregue o arquivo 
GRCh38_full_analysis_set_plus_decoy_hla.fa

* OBSERVAÇÃO : Certifique-se de que os arquivos CRAI e CRAM tenham o mesmo nome e verifique a integridade do download

# Uso

- No terminal, posicionado na pasta do projeto ative a env e execute o arquivo do pipeline 

source bioinformatics_venv/bin/activate

- Execute o script

python qc_pipeline.py

# Relatórios

- Todos os relatórios estarão na pasta output separados em: 

logs 
Na pasta logs será gerado o arquivo pipeline.log com o resultad

reports

# Implementações futuras

- Container
- Interface gráfica 
