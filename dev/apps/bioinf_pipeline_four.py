import argparse
import logging
import subprocess
import os
import glob
from dotenv import load_dotenv
from convert_files import convert_cram_to_bam
from coverage import calculate_coverage
from tqdm import tqdm
import matplotlib.pyplot as plt  # Importa matplotlib para gerar o histograma

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
    sample_output_dir = os.path.join(output_dir, sample_name)
    os.makedirs(sample_output_dir, exist_ok=True)

    # Configura o logging para a amostra específica
    sample_log_file = os.path.join(sample_output_dir, "logs", f"{sample_name}.log")
    os.makedirs(os.path.dirname(sample_log_file), exist_ok=True)
    sample_logger = logging.getLogger(sample_name)
    if not sample_logger.handlers:
        handler = logging.FileHandler(sample_log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        sample_logger.addHandler(handler)
        sample_logger.setLevel(logging.INFO)

    sample_logger.info(f"Iniciando processamento da amostra: {sample_name}")

    bam_file = os.path.join(intermediate_dir, "bam_files", f"{sample_name}.bam")
    os.makedirs(os.path.dirname(bam_file), exist_ok=True)
    try:
        with tqdm(total=1, desc=f"Convertendo {sample_name}", unit="amostra") as pbar:
            convert_cram_to_bam(cram_file, bam_file, samtools_path, ref_fasta)
            pbar.update(1)
    except Exception as e:
        sample_logger.error(f"Erro ao converter CRAM para BAM para a amostra {sample_name}: {e}")
        raise

    # Indexa o arquivo BAM
    try:
        subprocess.run([samtools_path, "index", bam_file], check=True)
        sample_logger.info(f"Arquivo BAM indexado: {bam_file}.bai")
    except subprocess.CalledProcessError as e:
        sample_logger.error(f"Erro ao indexar o arquivo BAM: {e}")
        raise

    # Calcula a cobertura usando o arquivo BAM gerado
    try:
        coverage_results = calculate_coverage(bam_file, bed_file, samtools_path)
        coverage_file_txt = os.path.join(sample_output_dir, "coverage_results.txt")
        coverage_file_png = os.path.join(sample_output_dir, "coverage_results.png") # Define o nome do arquivo para a imagem

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
        depths = [region['depth'] for region in coverage_results['region_coverage']] # Extrai as profundidades
        plt.hist(depths, bins=50)  # Cria o histograma
        plt.title('Distribuição da Profundidade de Cobertura')
        plt.xlabel('Profundidade de Cobertura')
        plt.ylabel('Frequência')
        plt.savefig(coverage_file_png)  # Salva o histograma como PNG
        plt.close() # Limpa o buffer de figura para evitar problemas com outras chamadas a plt
        sample_logger.info(f"Histograma de cobertura gerado e salvo em {coverage_file_png}")

    except Exception as e:
        sample_logger.error(f"Erro ao calcular a cobertura para a amostra {sample_name}: {e}")
        raise

    sample_logger.info(f"Processamento da amostra {sample_name} concluído")



def main(cram_dir, bed_file, output_dir, intermediate_dir,
         samtools_path="samtools", bcftools_path="bcftools", ref_fasta=None):
    """Executa o pipeline de controle de qualidade para múltiplos arquivos."""
    log_file = os.path.join(output_dir, "logs", "pipeline.log")
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
            process_one_sample(cram_file, bed_file, output_dir, intermediate_dir,
                               samtools_path, bcftools_path, ref_fasta)
        except Exception as e:
            logging.error(f"Erro ao processar a amostra {cram_file}: {e}")
            raise

    logging.info("Pipeline de controle de qualidade para múltiplos arquivos concluído")



if __name__ == "__main__":
    print('etapa0')
    parser = argparse.ArgumentParser(
        description="Pipeline de Controle de Qualidade de WES (Múltiplos Arquivos)")
    parser.add_argument("--cram_dir",
                        default=os.getenv("CRAM_FILES_DIR"),
                        help="Diretório contendo os arquivos CRAM")
    parser.add_argument("--bed",
                        default=os.getenv("BED_FILES_DIR"),
                        help="Caminho para o arquivo BED")
    parser.add_argument("--output_dir",
                        default=os.getenv("OUTPUT_DIR"),
                        help="Diretório de saída principal")
    parser.add_argument("--intermediate_dir",
                        default=os.getenv("INTERMEDIATE_DIR"),
                        help="Diretório intermediário")
    parser.add_argument("--samtools_path", default="samtools",
                        help="Caminho para samtools (opcional)")
    parser.add_argument("--bcftools_path", default="bcftools",
                        help="Caminho para bcftools (opcional)")
    parser.add_argument("--ref_fasta",
                        default=os.getenv("REF_GEN_FILE"),
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

