# dev/sex_inference.py
import subprocess
import logging

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