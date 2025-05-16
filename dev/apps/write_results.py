# dev/utils.py
import logging
import os

def write_results(output_dir, filename, results):
    """Escreve os resultados em um arquivo."""

    output_path = os.path.join(output_dir, filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(output_path, 'w') as f:
            if isinstance(results, dict):
                for key, value in results.items():
                    f.write(f"{key}: {value}\n")
            elif isinstance(results, list):
                for item in results:
                    f.write(f"{item}\n")
            else:
                f.write(str(results))
        logging.info(f"Resultados escritos em: {output_path}")
    except Exception as e:
        logging.error(f"Erro ao escrever resultados em {output_path}: {e}")
        raise