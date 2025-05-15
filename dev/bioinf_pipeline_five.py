import argparse
import logging
import os
import glob
import argparse 

from dotenv import load_dotenv
from sample_processing import process_one_sample

# diretório do arquivo atual
diretorio_arquivo = os.path.dirname(os.path.abspath(__file__))
# Pasta do projeto a partir desse script
project_dir = os.path.normpath(f"{diretorio_arquivo}{os.sep}..{os.sep}") + os.sep
# assim posso salvar os arquivos com seguraça em data

# Carrega as variáveis do arquivo .env
load_dotenv()

def setup_logging(log_file):
    """Configura o sistema de logging."""
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


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
