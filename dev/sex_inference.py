'''# dev/sex_inference.py
import subprocess
import logging

def calculate_chromosome_coverage(bam_file, chromosome, samtools_path="samtools"):
    """Calcula a cobertura média de um cromossomo específico."""

    try:
        #  samtools depth
        process = subprocess.Popen([samtools_path, "depth", "-r", chromosome, bam_file],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stderr:
            logging.error(f"Erro ao calcular cobertura do cromossomo {chromosome}: {stderr}")
            raise Exception(stderr)

        depths = [int(line.split('\t')[2]) for line in stdout.strip().split('\n')]
        average_depth = sum(depths) / len(depths) if depths else 0
        return average_depth

    except FileNotFoundError:
          logging.error(f"Ferramenta 'samtools' não encontrada. Verifique se está no PATH.")
          raise
    except Exception as e:
        logging.error(f"Erro ao executar o cálculo de cobertura do cromossomo: {e}")
        raise

def infer_sex(bam_file, samtools_path="samtools", bcftools_path="bcftools"):
    """Infere o sexo genético com base na cobertura dos cromossomos X e Y."""

    try:
        # Calcular cobertura dos cromossomos X e Y
        x_coverage = calculate_chromosome_coverage(bam_file, "X", samtools_path)
        y_coverage = calculate_chromosome_coverage(bam_file, "Y", samtools_path)

        # Inferir o sexo
        sex = "Unknown"
        if x_coverage > 0 and y_coverage == 0:
            sex = "Female"
        elif x_coverage > 0 and y_coverage > 0:
            sex = "Male"

        return {
            "x_coverage": x_coverage,
            "y_coverage": y_coverage,
            "predicted_sex": sex
        }

    except Exception as e:
        logging.error(f"Erro ao inferir sexo genético: {e}")
        raise
'''
'''
import subprocess
import logging
import re  # Importa o módulo de expressões regulares

def calculate_chromosome_coverage(bam_file, chromosome, samtools_path="samtools"):
    """Calcula a cobertura média de um cromossomo específico usando expressões regulares."""
    
    # Define a expressão regular para encontrar o cromossomo, aceitando diferentes prefixos
    chrom_regex = re.compile(rf"^chr?{chromosome}$", re.IGNORECASE)  # Aceita "X", "chrX", "x", "chrx"
    
    try:
        process = subprocess.Popen([samtools_path, "depth", bam_file],  # Remove o argumento '-r'
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        if stderr:
            logging.error(f"Erro ao calcular cobertura do cromossomo {chromosome}: {stderr}")
            raise Exception(stderr)
        
        total_depth = 0
        total_bases = 0
        
        for line in stdout.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) == 3:
                chrom, pos, depth = parts
                if chrom_regex.match(chrom):  # Usa a expressão regular para verificar o nome do cromossomo
                    total_depth += int(depth)
                    total_bases += 1
        
        average_depth = total_depth / total_bases if total_bases else 0
        logging.info(f"Cobertura do cromossomo {chromosome}: {average_depth:.2f}x")
        return average_depth

    except FileNotFoundError:
        logging.error(f"Ferramenta 'samtools' não encontrada. Verifique se está no PATH.")
        raise
    except ValueError:
        logging.error(f"Erro ao analisar a profundidade para o cromossomo {chromosome}.")
        raise
    except Exception as e:
        logging.error(f"Erro ao executar o cálculo de cobertura do cromossomo {chromosome}: {e}")
        raise



def infer_sex(bam_file, samtools_path="samtools", bcftools_path="bcftools"):
    """Infere o sexo genético com base na cobertura dos cromossomos X e Y."""
    
    try:
        x_coverage = calculate_chromosome_coverage(bam_file, "X", samtools_path)
        y_coverage = calculate_chromosome_coverage(bam_file, "Y", samtools_path)
        
        sex = "Unknown"
        if x_coverage > 0 and y_coverage == 0:
            sex = "Female"
        elif x_coverage > 0 and y_coverage > 0:
            sex = "Male"
        
        return {
            "x_coverage": x_coverage,
            "y_coverage": y_coverage,
            "predicted_sex": sex
        }
    
    except Exception as e:
        logging.error(f"Erro ao inferir sexo genético: {e}")
        raise
'''
'''
import subprocess
import logging
import re  # Importa o módulo de expressões regulares

def calculate_chromosome_coverage(bam_file, chromosome, samtools_path="samtools"):
    """Calcula a cobertura média de um cromossomo específico usando expressões regulares."""
    
    # Define a expressão regular para encontrar o cromossomo, aceitando diferentes prefixos
    chrom_regex = re.compile(rf"^chr?{chromosome}$", re.IGNORECASE)  # Aceita "X", "chrX", "x", "chrx"
    
    try:
        process = subprocess.Popen([samtools_path, "depth", "-m", "10000", bam_file],  # Adiciona a opção -m para limitar a profundidade
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        if stderr:
            logging.error(f"Erro ao calcular cobertura do cromossomo {chromosome}: {stderr}")
            raise Exception(stderr)
        
        total_depth = 0
        total_bases = 0
        
        for line in stdout.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) == 3:
                chrom, pos, depth = parts
                if chrom_regex.match(chrom):  # Usa a expressão regular para verificar o nome do cromossomo
                    total_depth += int(depth)
                    total_bases += 1
        
        average_depth = total_depth / total_bases if total_bases else 0
        logging.info(f"Cobertura do cromossomo {chromosome}: {average_depth:.2f}x")
        return average_depth

    except FileNotFoundError:
        logging.error(f"Ferramenta 'samtools' não encontrada. Verifique se está no PATH.")
        raise
    except ValueError:
        logging.error(f"Erro ao analisar a profundidade para o cromossomo {chromosome}.")
        raise
    except Exception as e:
        logging.error(f"Erro ao executar o cálculo de cobertura do cromossomo {chromosome}: {e}")
        raise



def infer_sex(bam_file, samtools_path="samtools", bcftools_path="bcftools"):
    """Infere o sexo genético com base na cobertura dos cromossomos X e Y."""
    
    try:
        x_coverage = calculate_chromosome_coverage(bam_file, "X", samtools_path)
        y_coverage = calculate_chromosome_coverage(bam_file, "Y", samtools_path)
        
        sex = "Unknown"
        if x_coverage > 0 and y_coverage == 0:
            sex = "Female"
        elif x_coverage > 0 and y_coverage > 0:
            sex = "Male"
        
        return {
            "x_coverage": x_coverage,
            "y_coverage": y_coverage,
            "predicted_sex": sex
        }
    
    except Exception as e:
        logging.error(f"Erro ao inferir sexo genético: {e}")
        raise
'''
'''
import subprocess
import logging
import re  # Importa o módulo de expressões regulares
import os
def calculate_chromosome_coverage(bam_file, chromosome, bed_file, samtools_path="samtools"):
    """Calcula a cobertura média de um cromossomo específico usando um arquivo BED."""

    # Define a expressão regular para encontrar o cromossomo, aceitando diferentes prefixos
    chrom_regex = re.compile(rf"^chr?{chromosome}$", re.IGNORECASE)

    try:
        # Cria um arquivo BED temporário contendo apenas o cromossomo de interesse
        temp_bed_file = f"{chromosome}_temp.bed"
        with open(temp_bed_file, "w") as f:
            # Aqui, assumimos que você tem um arquivo BED global (bed_file)
            # e itera sobre ele para extrair apenas as entradas do cromossomo alvo.
            with open(bed_file, "r") as global_bed:
                for line in global_bed:
                    parts = line.strip().split('\t')
                    if chrom_regex.match(parts[0]):  # Compara o nome do cromossomo do BED com regex
                        f.write(line)  # Escreve a linha do BED temporário

        process = subprocess.Popen([samtools_path, "bedcov", temp_bed_file, bam_file],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stderr:
            logging.error(f"Erro ao calcular cobertura do cromossomo {chromosome} com bedcov: {stderr}")
            raise Exception(stderr)

        total_coverage = 0
        total_bases = 0

        for line in stdout.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) >= 4:
                region_coverage = int(parts[-1])  # A cobertura está na última coluna
                region_start = int(parts[1])
                region_end = int(parts[2])
                total_coverage += region_coverage
                total_bases += (region_end - region_start)

        average_depth = total_coverage / total_bases if total_bases else 0
        logging.info(f"Cobertura do cromossomo {chromosome}: {average_depth:.2f}x")
        os.remove(temp_bed_file)  # Limpa o arquivo BED temporário
        return average_depth

    except FileNotFoundError:
        logging.error(f"Ferramenta 'samtools' não encontrada. Verifique se está no PATH.")
        raise
    except ValueError:
        logging.error(f"Erro ao analisar a profundidade para o cromossomo {chromosome}.")
        raise
    except Exception as e:
        logging.error(f"Erro ao executar o cálculo de cobertura do cromossomo {chromosome}: {e}")
        raise


def infer_sex(bam_file, bed_file, samtools_path="samtools", bcftools_path="bcftools"):
    """Infere o sexo genético com base na cobertura dos cromossomos X e Y."""

    try:
        x_coverage = calculate_chromosome_coverage(bam_file, "X", bed_file, samtools_path)
        y_coverage = calculate_chromosome_coverage(bam_file, "Y", bed_file, samtools_path)

        sex = "Unknown"
        if x_coverage > 0 and y_coverage == 0:
            sex = "Female"
        elif x_coverage > 0 and y_coverage > 0:
            sex = "Male"

        return {
            "x_coverage": x_coverage,
            "y_coverage": y_coverage,
            "predicted_sex": sex
        }

    except Exception as e:
        logging.error(f"Erro ao inferir sexo genético: {e}")
        raise'''


import subprocess
import logging
import re  # Importa o módulo de expressões regulares
import os
def calculate_chromosome_coverage(bam_file, chromosome, bed_file, samtools_path="samtools"):
    """Calcula a cobertura média de um cromossomo específico usando um arquivo BED."""

    # Define a expressão regular para encontrar o cromossomo, aceitando diferentes prefixos
    chrom_regex = re.compile(rf"^chr?{chromosome}$", re.IGNORECASE)

    try:
        # Cria um arquivo BED temporário contendo apenas o cromossomo de interesse
        temp_bed_file = f"{chromosome}_temp.bed"
        with open(temp_bed_file, "w") as f:
            # Aqui, assumimos que você tem um arquivo BED global (bed_file)
            # e itera sobre ele para extrair apenas as entradas do cromossomo alvo.
            with open(bed_file, "r") as global_bed:
                for line in global_bed:
                    parts = line.strip().split('\t')
                    if chrom_regex.match(parts[0]):  # Compara o nome do cromossomo do BED com regex
                        f.write(line)  # Escreve a linha do BED temporário

        process = subprocess.Popen([samtools_path, "bedcov", temp_bed_file, bam_file],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stderr:
            logging.error(f"Erro ao calcular cobertura do cromossomo {chromosome} com bedcov: {stderr}")
            raise Exception(stderr)

        total_coverage = 0
        total_bases = 0

        for line in stdout.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) >= 4:
                region_coverage = int(parts[-1])  # A cobertura está na última coluna
                region_start = int(parts[1])
                region_end = int(parts[2])
                total_coverage += region_coverage
                total_bases += (region_end - region_start)

        average_depth = total_coverage / total_bases if total_bases else 0
        logging.info(f"Cobertura do cromossomo {chromosome}: {average_depth:.2f}x")
        os.remove(temp_bed_file)  # Limpa o arquivo BED temporário
        return average_depth

    except FileNotFoundError:
        logging.error(f"Ferramenta 'samtools' não encontrada. Verifique se está no PATH.")
        raise
    except ValueError:
        logging.error(f"Erro ao analisar a profundidade para o cromossomo {chromosome}.")
        raise
    except Exception as e:
        logging.error(f"Erro ao executar o cálculo de cobertura do cromossomo {chromosome}: {e}")
        raise


def infer_sex(bam_file, bed_file, samtools_path="samtools", bcftools_path="bcftools"):
    """Infere o sexo genético com base na cobertura dos cromossomos X e Y."""

    try:
        x_coverage = calculate_chromosome_coverage(bam_file, "X", bed_file, samtools_path)
        y_coverage = calculate_chromosome_coverage(bam_file, "Y", bed_file, samtools_path)

        sex = "Inconclusivo"
        if x_coverage > 0 and y_coverage == 0:
            sex = "Feminino"
        elif x_coverage > 0 and y_coverage > 0:
            sex = "Masculino"

        return {
            "x_coverage": x_coverage,
            "y_coverage": y_coverage,
            "predicted_sex": sex
        }

    except Exception as e:
        logging.error(f"Erro ao inferir sexo genético: {e}")
        raise
