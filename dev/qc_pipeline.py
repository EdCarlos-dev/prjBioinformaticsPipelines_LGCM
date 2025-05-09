# dev/qc_pipeline.py
import argparse
import logging
import subprocess
import os
import glob
from dotenv import load_dotenv
from convert_files import convert_cram_to_bam
# from dev import (
#                  convert_files, 
#                 #  coverage, 
#                 #  sex_inference, 
#                 #  contamination,  
#                 #  write_results,
#                  )


# Carrega as variáveis do arquivo .env
load_dotenv()

def setup_logging(log_file):
    """Configura o sistema de logging."""
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def process_one_sample(cram_file, bed_file, output_dir, intermediate_dir,
                       samtools_path="samtools", bcftools_path="bcftools"):
    """Processa um único arquivo CRAM."""
    sample_name = os.path.splitext(os.path.basename(cram_file))[0]
    sample_output_dir = os.path.join(output_dir, sample_name)
    os.makedirs(sample_output_dir, exist_ok=True)

    logging.info(f"Iniciando processamento da amostra: {sample_name}")

    bam_file = os.path.join(intermediate_dir, "bam_files", f"{sample_name}.bam")
    os.makedirs(os.path.dirname(bam_file), exist_ok=True)
    convert_cram_to_bam(cram_file, bam_file, samtools_path)

    # coverage_results = coverage.calculate_coverage(bam_file, bed_file, samtools_path)
    # write_results.write_results(sample_output_dir, "coverage_results.txt", coverage_results)

    # sex_result = sex_inference.infer_sex(bam_file, samtools_path, bcftools_path)
    # write_results.write_results(sample_output_dir, "sex_inference.txt", sex_result)

    # contamination_result = contamination.estimate_contamination(bam_file)
    # write_results.write_results(sample_output_dir, "contamination.txt", contamination_result)  # Correção aqui

    logging.info(f"Processamento da amostra {sample_name} concluído")


def main(cram_dir, bed_file, output_dir, intermediate_dir,
         samtools_path="samtools", bcftools_path="bcftools"):
    """Executa o pipeline de controle de qualidade para múltiplos arquivos."""
    log_file = os.path.join(output_dir, "logs", "pipeline.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    setup_logging(log_file)

    logging.info("Início do pipeline de controle de qualidade para múltiplos arquivos")

    cram_files = glob.glob(os.path.join(cram_dir, "*.cram"))

    for cram_file in cram_files:
        process_one_sample(cram_file, bed_file, output_dir, intermediate_dir,
                           samtools_path, bcftools_path)

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

    args = parser.parse_args()

    #  Verifica se os diretórios obrigatórios foram fornecidos
    if not args.cram_dir:
        parser.error("--cram_dir é obrigatório")
    if not args.bed:
        parser.error("--bed é obrigatório")
    if not args.output_dir:
        parser.error("--output_dir é obrigatório")
    if not args.intermediate_dir:
        parser.error("--intermediate_dir é obrigatório")

    main(args.cram_dir, args.bed, args.output_dir, args.intermediate_dir,
         args.samtools_path, args.bcftools_path)