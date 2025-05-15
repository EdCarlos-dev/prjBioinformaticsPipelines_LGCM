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

## Estrutura do projto


## 3. 🛠️ Instruções de Uso

Instalação

- 1 - Ferramentas

Samtools
Bcftools

Use o código

```
bash
sudo apt-get install samtools bcftools
```

- 2 - Linguagens

Python 3.10.12

### 3.1. Clonando o repositório

```
bash
git clone https://github.com/seuusuario/repo.git
cd repo

```

### 3.2. Criando o Ambiente Virtual

```
python -m venv bioinformatics_venv
source bioinformatics_venv/bin/activate  # ou bioinformatics_venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### 3.3. Estrutura Esperada de Diretórios

```
data/
├── input/
│   ├── cram_files/        # Arquivos .cram
│   ├── bed_files/         # Arquivo BED com regiões de interesse
│   └── ref_gen_files/     # Genoma de referência (.fa e .fai)
├── intermediate/          # BAMs e arquivos intermediários
└── output/                # Relatórios finais e gráficos
```

### 3.4. Carregando os arquivos

Baixar os arquivos

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
GRCh38_full_analysis_set_plus_decoy_hla.fa 
Fonte - (https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/)

* OBSERVAÇÃO : Certifique-se de que os arquivos CRAI e CRAM tenham o mesmo nome e verifique a integridade do download


### 3.5. Executando o Pipeline

- No terminal, posicionado na pasta do projeto ative a env e execute o arquivo do pipeline 

```
python pipeline.py
```

## 4. 📦 Dependências e Ferramentas

samtools

bcftools

Python 3.10.12


## 5. 💻 Comandos de Exemplo

- Aqui temos um modo de usar o pipeline usando argumentos presentes no script , onde é possível apontar para um path ou arquivos diferentespara uso

bash
```
python pipeline.py \
  --cram_dir data/input/cram_files \
  --bed data/input/bed_files/meu_exoma.bed \
  --ref_fasta data/input/ref_gen_files/GRCh38.fa \
  --output_dir data/output \
  --intermediate_dir data/intermediate
```

- Ou simplesmente o uso da estrutura de pastas e arquivos de configuração já existentes

bash
```
python pipeline.py
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
Amostra: NA06994

Profundidade média	54.6x

% coberto ≥ 10x	99.2%

% coberto ≥ 30x	94.8%

Cobertura cromossomo X	50.2x

Cobertura cromossomo Y	0.0x

Sexo genético estimado	Feminino (XX)

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