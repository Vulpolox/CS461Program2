import sys
sys.path.append("src")

from pathlib import Path
from genetic_algorithm import genetic_algorithm

def main():
    out_file_path = Path(__file__).resolve().parent / 'output' / 'output.txt'
    log_file_path = Path(__file__).resolve().parent / 'output' / 'log.txt'

    ga = genetic_algorithm()

    with open(out_file_path, "w") as out_file, open(log_file_path, "w") as log_file:
        ga.run(log_file, out_file)

if __name__ == "__main__":
    main()