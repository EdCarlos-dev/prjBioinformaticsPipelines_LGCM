
import argparse
import logging
import subprocess
import os
import glob
import argparse 
from tqdm import tqdm
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from convert_files import convert_cram_to_bam
from coverage import calculate_coverage
from sex_inference import infer_sex

# diretório do arquivo atual
diretorio_arquivo = os.path.dirname(os.path.abspath(__file__))
# Pasta do projeto a partir desse script
project_dir = os.path.normpath(f"{diretorio_arquivo}{os.sep}..{os.sep}") + os.sep
# assim posso salvar os arquivos com seguraça em data
# print(project_dir)


# definir o caminho do arquivo atual e concatenar com as strings da env
# Carrega as variáveis do arquivo .env
load_dotenv()

def setup_logging(log_file):
    """Configura o sistema de logging."""
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def process_one_sample(cram_file, bed_file, output_dir, intermediate_dir,
                       samtools_path="samtools", bcftools_path="bcftools", ref_fasta=None):

    """Processa um único arquivo CRAM."""
    sample_name = os.path.splitext(os.path.basename(cram_file))[0]
    sample_output_dir = os.path.join(output_dir, "reports", sample_name)
    os.makedirs(sample_output_dir, exist_ok=True)

    # Configura o logging para a amostra específica
    sample_log_file = os.path.join(sample_output_dir, "logs", f"logs_{sample_name}.log")
    os.makedirs(os.path.dirname(sample_log_file), exist_ok=True)
    sample_logger = logging.getLogger(sample_name)
    if not sample_logger.handlers:
        handler = logging.FileHandler(sample_log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        sample_logger.addHandler(handler)
        sample_logger.setLevel(logging.INFO)
    
    print(f'Processando amostra: {sample_name}')

    sample_logger.info(f"Iniciando processamento da amostra: {sample_name}")

    bam_file = os.path.join(intermediate_dir, "bam_files", f"{sample_name}.bam")
    os.makedirs(os.path.dirname(bam_file), exist_ok=True)

    
    try:
        if os.path.exists(bam_file):
            sample_logger.info(f"Arquivo BAM já existe: {bam_file}")
            print(f"Arquivo BAM já existe: {bam_file}")

        else:
        
            print(f'Convertendo CRAM para BAM: {cram_file} -> {bam_file}')
            with tqdm(total=1, desc=f"Convertendo {sample_name}", unit="amostra") as pbar:
                convert_cram_to_bam(cram_file, bam_file, samtools_path, ref_fasta)
                pbar.update(1)

    except Exception as e:
        sample_logger.error(f"Erro ao converter CRAM para BAM para a amostra {sample_name}: {e}")
        raise

    # Indexa o arquivo BAM
    try:
        # Verifica se o arquivo BAM já está indexado
        bam_index_file = f"{bam_file}.bai"
        if os.path.exists(bam_index_file):
            sample_logger.info(f"Arquivo BAM já indexado: {bam_index_file}")
            print(f"Arquivo BAM já indexado: {bam_index_file}")

        else:
    
            # Indexa o arquivo BAM
            print(f'Indexando arquivo BAM: {bam_file}')
            subprocess.run([samtools_path, "index", bam_file], check=True)
            sample_logger.info(f"Arquivo BAM indexado: {bam_file}.bai")
    except subprocess.CalledProcessError as e:
        sample_logger.error(f"Erro ao indexar o arquivo BAM: {e}")
        raise

    # Calcula a cobertura usando o arquivo BAM gerado
    print(f'Calculando cobertura para a amostra: {sample_name}')
    try:
        coverage_results = calculate_coverage(bam_file, bed_file, samtools_path)
        coverage_file_txt = os.path.join(sample_output_dir, f"coverage_{sample_name}_results.txt")
        coverage_file_png = os.path.join(sample_output_dir, f"coverage_{sample_name}_results.png")

        # Salva os resultados em um arquivo de texto
        with open(coverage_file_txt, "w") as f:
            f.write(f"Profundidade Média: {coverage_results['mean_depth']:.2f}x\n")
            f.write(f"% Coberto >= 10x: {coverage_results['percent_covered_10x']:.2f}%\n")
            f.write(f"% Coberto >= 30x: {coverage_results['percent_covered_30x']:.2f}%\n")
            f.write("\nCobertura por Região:\n")
            f.write("Cromossomo\tInício\tFim\tProfundidade\n")
            for region in coverage_results['region_coverage']:
                f.write(f"{region['chrom']}\t{region['start']}\t{region['end']}\t{region['depth']}x\n")
        sample_logger.info(f"Cobertura calculada e salva em {coverage_file_txt}")

        # Gera o histograma e salva em um arquivo PNG
        depths = [region['depth'] for region in coverage_results['region_coverage']]
        plt.hist(depths, bins=50)
        plt.title('Distribuição da Profundidade de Cobertura')
        plt.xlabel('Profundidade de Cobertura')
        plt.ylabel('Frequência')
        plt.savefig(coverage_file_png)
        plt.close()
        sample_logger.info(f"Histograma de cobertura gerado e salvo em {coverage_file_png}")

    except Exception as e:
        sample_logger.error(f"Erro ao calcular a cobertura para a amostra {sample_name}: {e}")
        raise
    

    # Estima o sexo genético
    print(f'Inferindo sexo genético para a amostra: {sample_name}')
    try:
        sex_inference_results = infer_sex(bam_file, bed_file, samtools_path, bcftools_path)
        sex_inference_file = os.path.join(sample_output_dir, f"sex_inference_{sample_name}.txt")
        with open(sex_inference_file, "w") as f:
            f.write(f"Cromossomo X Cobertura: {sex_inference_results['x_coverage']:.2f}x\n")
            f.write(f"Cromossomo Y Cobertura: {sex_inference_results['y_coverage']:.2f}x\n")
            f.write(f"Sexo Predito: {sex_inference_results['predicted_sex']}\n")
        sample_logger.info(f"Sexo genético inferido e salvo em {sex_inference_file}")

    except Exception as e:
        sample_logger.error(f"Erro ao inferir o sexo genético para a amostra {sample_name}: {e}")
        raise
    
    print(f'Processamento da amostra {sample_name} concluído')

    sample_logger.info(f"Processamento da amostra {sample_name} concluído")


def main(cram_dir, bed_file, output_dir, intermediate_dir,
         samtools_path="samtools", bcftools_path="bcftools", ref_fasta=None):
    """Executa o pipeline de controle de qualidade para múltiplos arquivos."""
    log_file = f'{output_dir}{os.sep}logs{os.sep}pipeline.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    setup_logging(log_file)

    logging.info("Início do pipeline de controle de qualidade para múltiplos arquivos")

    # Verifica se os diretórios e arquivos existem
    if not os.path.exists(cram_dir):
        logging.error(f"Diretório CRAM não encontrado: {cram_dir}")
        raise FileNotFoundError(f"Diretório CRAM não encontrado: {cram_dir}")
    if not os.path.exists(bed_file):
        logging.error(f"Arquivo BED não encontrado: {bed_file}")
        raise FileNotFoundError(f"Arquivo BED não encontrado: {bed_file}")
    if not os.path.exists(output_dir):
        logging.error(f"Diretório de saída não encontrado: {output_dir}")
        os.makedirs(output_dir)
    if not os.path.exists(intermediate_dir):
        logging.error(f"Diretório intermediário não encontrado: {intermediate_dir}")
        os.makedirs(intermediate_dir)

    cram_files = glob.glob(os.path.join(cram_dir, "*.cram"))
    if not cram_files:
        logging.error(f"Nenhum arquivo CRAM encontrado em: {cram_dir}")
        raise FileNotFoundError(f"Nenhum arquivo CRAM encontrado em: {cram_dir}")

    for cram_file in cram_files:
        try: 
            # verificar antes se o arquivo cram já foi processado 
            process_one_sample(cram_file, bed_file, output_dir, intermediate_dir,
                               samtools_path, bcftools_path, ref_fasta)
        except Exception as e:
            logging.error(f"Erro ao processar a amostra {cram_file}: {e}")
            raise

    logging.info("Pipeline de controle de qualidade para múltiplos arquivos concluído")



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Pipeline de Controle de Qualidade de WES (Múltiplos Arquivos)")
    parser.add_argument("--cram_dir",
                        default=f'{project_dir}data{os.sep}input{os.sep}cram_files',
                        help="Diretório contendo os arquivos CRAM")
    parser.add_argument("--bed",
                        default=f'{project_dir}data{os.sep}input{os.sep}bed_files{os.sep}{os.getenv("BED_FILE_NAME")}',
                        help="Caminho para o arquivo BED")
    parser.add_argument("--output_dir",
                        default=f'{project_dir}data{os.sep}output',
                        help="Diretório de saída principal")
    parser.add_argument("--intermediate_dir",
                        default=f'{project_dir}data{os.sep}intermediate',
                        help="Diretório intermediário")
    parser.add_argument("--samtools_path", default="samtools",
                        help="Caminho para samtools (opcional)")
    parser.add_argument("--bcftools_path", default="bcftools",
                        help="Caminho para bcftools (opcional)")
    parser.add_argument("--ref_fasta",
                        default=f'{project_dir}data{os.sep}input{os.sep}ref_gen_files{os.sep}{os.getenv("REF_GEN_FILE_NAME")}',
                        help="Caminho para o arquivo FASTA do genoma de referência (opcional)")

    args = parser.parse_args()

    # Verifica se os diretórios obrigatórios foram fornecidos
    if not args.cram_dir:
        parser.error("--cram_dir é obrigatório")
    if not args.bed:
        parser.error("--bed é obrigatório")
    if not args.output_dir:
        parser.error("--output_dir é obrigatório")
    if not args.intermediate_dir:
        parser.error("--intermediate_dir é obrigatório")

    try:
        main(args.cram_dir, args.bed, args.output_dir, args.intermediate_dir,
             args.samtools_path, args.bcftools_path, args.ref_fasta)
    except Exception as e:
        print(f"Erro durante a execução do pipeline: {e}")
        exit(1)
