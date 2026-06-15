import asyncio
import sys
import warnings
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq")
import logging
logging.getLogger("IPKernelApp").setLevel(logging.ERROR)

import os
import sys
import nbformat
from nbformat.validator import normalize
from nbconvert.preprocessors import ExecutePreprocessor

VALID_MODES = {"original", "modified"}
DEFAULT_MODE = "original"


def run_notebook_from_cell(
    notebook_path: str,
    start_cell_index: int,
    output_path: str = None,
    kernel_name: str = "python3",
    timeout: int = 600,
    mode: str = DEFAULT_MODE,
):
    os.environ["MODE"] = mode

    with open(notebook_path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    nb.nbformat_minor = 5
    _, nb = normalize(nb)
    nb.cells = nb.cells[start_cell_index:]

    print(f"Iniciando ejecución con MODE='{mode}'...")

    ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name)
    ep.preprocess(nb, {"metadata": {"path": os.path.dirname(os.path.abspath(notebook_path))}})

    print(f"Notebook ejecutado con MODE='{mode}'")


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    mode = DEFAULT_MODE

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode not in VALID_MODES:
            print(f"[ERROR] Modo inválido: '{mode}'. Opciones: {', '.join(VALID_MODES)}")
            sys.exit(1)

    run_notebook_from_cell(
        notebook_path=os.path.join(SCRIPT_DIR, "TFG.ipynb"),
        start_cell_index=4,
        mode=mode,
    )


if __name__ == "__main__":
    main()
