import sys
import runpy
import os

# Adiciona o diretório src ao path se não estiver lá
src_path = os.path.join(os.path.dirname(__file__), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

if __name__ == "__main__":
    runpy.run_module("draw", run_name="__main__")
