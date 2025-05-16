# dev/panelmapcreate.py

import os
import subprocess
import logging

# Não implementado

def prepare_verifybamid_panel(chromossome_dir, intermediate_dir, output_name):
    """
    Concatena arquivos .vcf.gz válidos com bcftools e salva painel final para uso no VerifyBamID.
    Caminhos devem ser absolutos.
    """
    chromossome_dir = os.path.abspath(chromossome_dir)
    intermediate_dir = os.path.abspath(intermediate_dir)
    os.makedirs(intermediate_dir, exist_ok=True)
    output_path = os.path.join(intermediate_dir, output_name)

    # Filtra apenas arquivos .vcf.gz (ignora .tbi e outros)
    vcf_files = sorted([
        os.path.join(chromossome_dir, f)
        for f in os.listdir(chromossome_dir)
        if f.endswith(".vcf.gz")
    ])

    if not vcf_files:
        raise FileNotFoundError(f"Nenhum arquivo .vcf.gz encontrado em {chromossome_dir}")

    print(f"🔗 Concatenando {len(vcf_files)} arquivos VCF com bcftools...")

    try:
        # Concatenar os arquivos
        cmd_concat = ["bcftools", "concat", "-Oz", "-o", output_path] + vcf_files
        subprocess.run(cmd_concat, check=True)

        # Indexar com tabix
        subprocess.run(["tabix", "-p", "vcf", output_path], check=True)

        print(f"✅ Painel VCF gerado: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao gerar painel VCF: {e}")
        raise


# Execução direta para testes
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cria painel VCF concatenado para uso com VerifyBamID")
    parser.add_argument("--chromossome_dir", required=True, help="Diretório com arquivos .vcf.gz por cromossomo")
    parser.add_argument("--intermediate_dir", required=True, help="Diretório de saída para o painel final")
    parser.add_argument("--output_name", default="merged_panel.vcf.gz", help="Nome do painel final (default: merged_panel.vcf.gz)")

    args = parser.parse_args()

    try:
        prepare_verifybamid_panel(
            chromossome_dir=args.chromossome_dir,
            intermediate_dir=args.intermediate_dir,
            output_name=args.output_name
        )
    except Exception as e:
        print(f"❌ Erro: {e}")
