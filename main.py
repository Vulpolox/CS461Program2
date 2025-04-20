import sys
sys.path.append("src")

from schedule import schedule
import data

def main():
    s = schedule()
    print(f'FITNESS:\n---\n{s.fitness}')

if __name__ == "__main__":
    main()