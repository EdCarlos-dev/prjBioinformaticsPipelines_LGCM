import logging
import subprocess


def run_command(command, log_message):
    """Executa um comando de linha de comando e trata erros."""
    try:
        logging.info(f"Executando: {log_message}")
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar {log_message}: {e.stderr}")
        raise


'''# scripts separados
def convert_cram_to_bam(cram_file, output_bam, samtools_path="samtools"):
    """Converte CRAM para BAM usando samtools."""
    run_command(
        [samtools_path, "view", "-b", "-o", output_bam, cram_file],
        f"Conversão de CRAM para BAM: {cram_file} -> {output_bam}"
    )
    logging.info(f"CRAM convertido para BAM: {output_bam}")
'''
def convert_cram_to_bam(cram_file, output_bam, samtools_path="samtools", ref_fasta=None): # Adiciona ref_fasta
    """Converte CRAM para BAM usando samtools."""
    command = [samtools_path, "view", "-b", "-o", output_bam]
    if ref_fasta:  # Adiciona a opção -T se ref_fasta for fornecido
        command.extend(["-T", ref_fasta])
    command.append(cram_file)
    run_command(
        command,
        f"Conversão de CRAM para BAM: {cram_file} -> {output_bam}"
    )
    logging.info(f"CRAM convertido para BAM: {output_bam}")


# scripts separados
def convert_bam_to_fastq(bam_file, output_fastq_prefix, samtools_path="samtools"):
    """Converte BAM para FASTQ usando samtools."""

    #  Determina os nomes dos arquivos FASTQ de saída
    fastq_file_R1 = f"{output_fastq_prefix}_R1.fastq"
    fastq_file_R2 = f"{output_fastq_prefix}_R2.fastq"

    try:
        #  samtools fastq -1 para R1, -2 para R2
        process_R1 = subprocess.Popen([samtools_path, "fastq", "-1", fastq_file_R1, bam_file],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process_R2 = subprocess.Popen([samtools_path, "fastq", "-2", fastq_file_R2, bam_file],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        stdout_R1, stderr_R1 = process_R1.communicate()
        stdout_R2, stderr_R2 = process_R2.communicate()

        if stderr_R1 or stderr_R2:
            logging.error(f"Erro ao converter BAM para FASTQ: {stderr_R1 or stderr_R2}")
            raise Exception(stderr_R1 or stderr_R2)

        logging.info(f"BAM convertido para FASTQ: {fastq_file_R1}, {fastq_file_R2}")

    except FileNotFoundError:
        logging.error(f"Ferramenta 'samtools' não encontrada. Verifique se está no PATH.")
        raise
    except Exception as e:
        logging.error(f"Erro ao converter BAM para FASTQ: {e}")
        raise
