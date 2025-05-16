import os
import subprocess
import threading
import time
from tqdm import tqdm

def index_bam_with_progress(bam_file, samtools_path="samtools"):
    """Indexa um arquivo BAM com samtools e exibe uma barra de progresso simulada."""
    bai_file = bam_file + ".bai"
    estimated_time = 10  # segundos (ajustável)

    pbar = tqdm(total=estimated_time, desc="Indexando BAM", bar_format="{desc}: {elapsed} elapsed", colour='green')
    stop_event = threading.Event()

    def fake_progress():
        for _ in range(estimated_time):
            if stop_event.is_set():
                break
            pbar.update(1)
            time.sleep(1)

    def wait_for_index():
        while not stop_event.is_set():
            if os.path.exists(bai_file):
                stop_event.set()
                break
            time.sleep(0.5)

    try:
        thread1 = threading.Thread(target=fake_progress)
        thread2 = threading.Thread(target=wait_for_index)
        thread1.start()
        thread2.start()

        subprocess.run([samtools_path, "index", bam_file], check=True)

        thread1.join()
        thread2.join()

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro ao indexar BAM: {e}")
    finally:
        pbar.n = estimated_time
        pbar.refresh()
        pbar.close()
