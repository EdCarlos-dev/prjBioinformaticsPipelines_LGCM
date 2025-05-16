import logging
import subprocess
import os
'''def run_command(command, log_message):
    """Executa um comando de linha de comando e trata erros."""
    try:
        logging.info(f"Executando: {log_message}")
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar {log_message}: {e.stderr}")
        raise'''

'''def run_command(command, log_message):
    """Executa um comando de linha de comando e exibe saída em tempo real."""
    logging.info(f"Executando: {log_message}")
    print(f"\n[Início] {log_message}\n")

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # Exibe o stderr (normalmente onde samtools escreve logs)
    for line in process.stderr:
        print(f"[samtools] {line.strip()}")

    process.wait()

    if process.returncode != 0:
        logging.error(f"Erro ao executar {log_message}")
        raise subprocess.CalledProcessError(process.returncode, command)

    print(f"\n[✔] Finalizado: {log_message}\n")
'''
'''
def run_command(command, log_message):
    """Executa um comando de linha de comando e permite barra de progresso do samtools."""
    logging.info(f"Executando: {log_message}")
    print(f"\n[Início] {log_message}\n")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar {log_message}")
        raise

    print(f"\n[✔] Finalizado: {log_message}\n")'''
################################
import os
import time
import logging
import threading
from tqdm import tqdm


def estimate_bam_size_bytes(cram_path, ratio=3.0):
    """Estima o tamanho do BAM com base no tamanho do CRAM."""
    cram_size = os.path.getsize(cram_path)
    return int(cram_size * ratio)


def run_command_with_progress(command_list, bam_path, estimated_size, log_message):
    """Executa comando via shell e exibe barra de progresso baseada no crescimento do arquivo BAM."""
    logging.info(f"Executando: {log_message}")
    print(f"\n[Início] {log_message}\n")

    # Barra de progresso
    pbar = tqdm(total=estimated_size,
                colour='green', 
                unit='B', 
                unit_scale=True, 
                desc="Convertendo CRAM → BAM",
                bar_format="{desc}: {bar} {percentage:3.0f}% | {elapsed} elapsed"
            )
    stop_event = threading.Event()

    def monitor_bam_growth():
        while not stop_event.is_set():
            if os.path.exists(bam_path):
                actual_size = os.path.getsize(bam_path)
                pbar.n = min(actual_size, estimated_size)
                pbar.refresh()
            time.sleep(1)

    monitor_thread = threading.Thread(target=monitor_bam_growth)
    monitor_thread.start()

    try:
        # Usa os.system apenas para manter compatível com seu código atual
        exit_code = os.system(" ".join(command_list))
        if exit_code != 0:
            raise RuntimeError(f"Erro ao executar: {log_message}")
    finally:
        stop_event.set()
        monitor_thread.join()
        pbar.n = estimated_size
        pbar.refresh()
        pbar.close()

    print(f"\n[✔] Finalizado: {log_message}\n")


def convert_cram_to_bam(cram_file, output_bam, samtools_path="samtools", ref_fasta=None):
    """Converte CRAM para BAM usando samtools (sem ordenação), com barra de progresso."""
    estimated_bam_size = estimate_bam_size_bytes(cram_file)

    command = [samtools_path, "view", "-b", "-o", output_bam]
    if ref_fasta:
        command.extend(["-T", ref_fasta])
    command.append(cram_file)

    run_command_with_progress(
        command,
        output_bam,
        estimated_bam_size,
        f"Conversão de CRAM para BAM: {cram_file} -> {output_bam}"
    )

    logging.info(f"CRAM convertido para BAM: {output_bam}")

################################
'''
def run_command(command, log_message):
    """Executa comando via shell para permitir barra de progresso do samtools."""
    logging.info(f"Executando: {log_message}")
    print(f"\n[Início] {log_message}\n")

    exit_code = os.system(" ".join(command))
    if exit_code != 0:
        raise RuntimeError(f"Erro ao executar: {log_message}")

    print(f"\n[✔] Finalizado: {log_message}\n")



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
'''

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
