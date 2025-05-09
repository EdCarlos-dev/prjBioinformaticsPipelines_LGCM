# dev/coverage.py
import subprocess
import logging

def calculate_coverage(bam_file, bed_file, samtools_path="samtools"):
    """Calcula a cobertura nas regiões exônicas."""

    try:
        # Use samtools bedcov
        process = subprocess.Popen([samtools_path, "bedcov", bed_file, bam_file],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stderr:
            logging.error(f"Erro ao calcular cobertura: {stderr}")
            raise Exception(stderr)

        coverage_data = parse_bedcov_output(stdout)
        return coverage_data

    except FileNotFoundError:
        logging.error(f"Ferramenta 'samtools' não encontrada. Verifique se está no PATH.")
        raise
    except Exception as e:
        logging.error(f"Erro ao executar o cálculo de cobertura: {e}")
        raise

def parse_bedcov_output(output):
    """Analisa a saída do samtools bedcov."""

    results = []
    total_bases = 0
    covered_10x = 0
    covered_30x = 0

    for line in output.strip().split('\n'):
        parts = line.split('\t')
        chrom, start, end, _, _, depth = parts
        start = int(start)
        end = int(end)
        depth = int(depth)
        region_length = end - start

        total_bases += region_length
        if depth >= 10:
            covered_10x += region_length
        if depth >= 30:
            covered_30x += region_length

        results.append({
            'chrom': chrom,
            'start': start,
            'end': end,
            'depth': depth
        })

    mean_depth = sum(region['depth'] * (region['end'] - region['start']) for region in results) / total_bases if total_bases else 0
    percent_10x = (covered_10x / total_bases) * 100 if total_bases else 0
    percent_30x = (covered_30x / total_bases) * 100 if total_bases else 0

    return {
        'mean_depth': mean_depth,
        'percent_covered_10x': percent_10x,
        'percent_covered_30x': percent_30x,
        'region_coverage': results
    }