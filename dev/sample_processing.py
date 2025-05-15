import logging
import subprocess
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

from convert_files import convert_cram_to_bam
from coverage import calculate_coverage
from sex_inference import infer_sex


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
