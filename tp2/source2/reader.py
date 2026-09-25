import shutil
from datetime import datetime
from pathlib import Path

# Dossier contenant les CSV du TP1
SOURCE_DIR = Path("../../data")  # TP1: tp-audit-cartographie/data/
# Dossier de sortie dans le Data Lake
OUTPUT_DIR = Path("../datalake/raw/source2")

FILES = ["results.csv", "goalscorers.csv", "shootouts.csv", "former_names.csv"]


def run():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    for filename in FILES:
        src = SOURCE_DIR / filename
        if not src.exists():
            print(f"Fichier manquant, ignoré : {src}")
            continue
        dst = run_dir / filename
        shutil.copy2(src, dst)
        print(f"Copié : {filename} -> {dst}")

    print(f"Source 2 archivée dans {run_dir}")


if __name__ == "__main__":
    run()